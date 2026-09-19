document.addEventListener("alpine:init", () => {
  const WISHLIST_KEY = "fitile_shop_wishlist";

  const getCsrfToken = () => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute("content");
    const input = document.querySelector("[name=csrfmiddlewaretoken]");
    return input ? input.value : "";
  };

  const loadWishlist = () => {
    try {
      const data = localStorage.getItem(WISHLIST_KEY);
      if (data) return JSON.parse(data);
    } catch (e) {
      /* ignore */
    }
    return [];
  };

  const saveWishlist = (items) =>
    localStorage.setItem(WISHLIST_KEY, JSON.stringify(items));

  const cartCountFrom = (items) =>
    items.reduce((sum, item) => sum + (item.qty || item.quantity || 0), 0);

  const postCartRequest = async (url, fields) => {
    const body = new FormData();
    Object.entries(fields).forEach(([key, value]) => body.append(key, value));
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCsrfToken(),
        "X-Requested-With": "XMLHttpRequest",
      },
      body,
    });
    return res.json();
  };

  Alpine.store("app", {
    wishlist: loadWishlist(),

    toggleWishlist(slug) {
      const index = this.wishlist.indexOf(slug);
      if (index > -1) {
        this.wishlist.splice(index, 1);
      } else {
        this.wishlist.push(slug);
      }
      saveWishlist([...this.wishlist]);
    },

    isWishlisted(slug) {
      return this.wishlist.includes(slug);
    },
  });

  Alpine.data("appStore", () => ({
    loading: true,
    searchOpen: false,
    cartOpen: false,
    mobileMenuOpen: false,
    headerSticky: false,
    cartItems: [],

    get cartCount() {
      return cartCountFrom(this.cartItems);
    },

    init() {
      window.addEventListener("load", () => {
        setTimeout(() => {
          this.loading = false;
        }, 600);
      });
      setTimeout(() => {
        this.loading = false;
      }, 1200);
      window.addEventListener("scroll", () => {
        this.headerSticky = window.scrollY > 40;
      });
      this.fetchCart();
    },

    async fetchCart() {
      try {
        const res = await fetch("/shop/cart/api/");
        const data = await res.json();
        if (data.ok) {
          this.cartItems = data.items || [];
        }
      } catch (e) {
        /* ignore */
      }
    },

    applyCartResponse(data) {
      if (data.ok) {
        this.cartItems = data.items || [];
      }
    },

    openSearch() {
      this.searchOpen = true;
      this.cartOpen = false;
      this.mobileMenuOpen = false;
      document.body.style.overflow = "hidden";
    },

    openCart() {
      this.cartOpen = true;
      this.searchOpen = false;
      this.mobileMenuOpen = false;
      document.body.style.overflow = "hidden";
    },

    closeAllModals() {
      this.searchOpen = false;
      this.cartOpen = false;
      this.mobileMenuOpen = false;
      document.body.style.overflow = "";
    },

    toggleWishlist(slug) {
      Alpine.store("app").toggleWishlist(slug);
    },

    isWishlisted(slug) {
      return Alpine.store("app").isWishlisted(slug);
    },

    async addToCart(product) {
      const variantId = product.variant_id;
      const slug = product.slug;
      if (!variantId || !slug) {
        window.location.href = product.url || "/shop/products/";
        return false;
      }
      const qty = product.qty || 1;
      try {
        const data = await postCartRequest(`/shop/cart/add/${slug}/`, {
          variant_id: variantId,
          quantity: qty,
        });
        if (data.ok) {
          this.applyCartResponse(data);
          this.openCart();
          return true;
        }
        alert(data.error || "خطا در افزودن به سبد");
        return false;
      } catch (e) {
        alert("خطا در اتصال به سرور");
        return false;
      }
    },

    async removeFromCart(variantId) {
      try {
        const data = await postCartRequest(`/shop/cart/remove/${variantId}/`, {});
        this.applyCartResponse(data);
      } catch (e) {
        /* ignore */
      }
    },

    async updateQty(item, delta) {
      const qty = item.qty || item.quantity || 1;
      const newQty = Math.max(0, qty + delta);
      const id = item.id || item.variant_id;
      try {
        if (newQty < 1) {
          await this.removeFromCart(id);
          return;
        }
        const data = await postCartRequest(`/shop/cart/update/${id}/`, {
          quantity: newQty,
        });
        if (data.ok) {
          this.applyCartResponse(data);
        } else {
          alert(data.error || "خطا");
        }
      } catch (e) {
        /* ignore */
      }
    },

    cartTotal() {
      return this.cartItems.reduce(
        (sum, item) => sum + (item.line_total || 0),
        0,
      );
    },

    formatPrice(num) {
      const n = Number(num);
      if (!Number.isFinite(n)) return "۰";
      return Math.round(n).toLocaleString("fa-IR");
    },
  }));

  Alpine.data("heroSlider", (opts = {}) => ({
    current: 0,
    themes: opts.themes || ["photo"],
    timer: null,

    init() {
      this.startAutoplay();
    },

    shellClass() {
      const theme = this.themes[this.current] || "photo";
      return `hero-shell--${theme}`;
    },

    next() {
      this.current = (this.current + 1) % Math.max(this.themes.length, 1);
    },

    prev() {
      const n = Math.max(this.themes.length, 1);
      this.current = (this.current - 1 + n) % n;
    },

    go(i) {
      this.current = i;
    },

    startAutoplay() {
      this.stopAutoplay();
      if (this.themes.length < 2) return;
      this.timer = setInterval(() => this.next(), 7000);
    },

    stopAutoplay() {
      if (this.timer) clearInterval(this.timer);
      this.timer = null;
    },
  }));

  Alpine.data("wishlistPage", () => ({
    slugs: loadWishlist(),
    remove(slug) {
      Alpine.store("app").toggleWishlist(slug);
      this.slugs = loadWishlist();
    },
  }));

  Alpine.data("productDetailPage", () => {
    const el = document.getElementById("fitile-product-data");
    let product = {};
    try {
      product = el ? JSON.parse(el.textContent) : {};
    } catch (e) {
      product = {};
    }
    if (typeof product !== "object" || product === null) {
      product = {};
    }

    const sizes = product.sizes || [];
    const colors = product.colors || [];

    return {
      product,
      qty: 1,
      tab: "desc",
      selectedSize: sizes[0] || "",
      selectedColor: (colors[0] && colors[0].name) || "",
      imageIndex: 0,
      gallery: product.gallery || [],

      get currentImage() {
        if (this.gallery[this.imageIndex] && this.gallery[this.imageIndex].url) {
          return this.gallery[this.imageIndex].url;
        }
        return product.image_url || "";
      },

      get activeVariant() {
        const matrix = product.variant_matrix || {};
        const key = `${this.selectedSize}|${this.selectedColor || ""}`;
        if (matrix[key]) return matrix[key];
        const bySize = Object.values(matrix).find(
          (v) => v && v.size === this.selectedSize,
        );
        if (bySize) return bySize;
        const values = Object.values(matrix);
        return values.length ? values[0] : null;
      },

      get activePrice() {
        if (this.activeVariant && this.activeVariant.effective_price != null) {
          return this.activeVariant.effective_price;
        }
        return product.effective_price_num || product.price_num || 0;
      },

      get activeBase() {
        if (this.activeVariant && this.activeVariant.price != null) {
          return this.activeVariant.price;
        }
        return product.price_num || 0;
      },

      get activeSale() {
        const sale = this.activeVariant && this.activeVariant.sale_price;
        return Boolean(sale && sale < this.activeBase);
      },

      get canAdd() {
        if (!this.activeVariant) return Boolean(product.default_variant_id);
        return this.activeVariant.stock > 0;
      },

      selectSize(size) {
        this.selectedSize = size;
      },

      selectColor(name) {
        this.selectedColor = name;
      },

      selectImage(index) {
        this.imageIndex = index;
      },

      formatPrice(num) {
        const n = Number(num);
        if (!Number.isFinite(n)) return "۰";
        return Math.round(n).toLocaleString("fa-IR");
      },

      async add() {
        if (!this.canAdd) return;
        const variantId =
          (this.activeVariant && this.activeVariant.id) ||
          product.default_variant_id;
        if (!variantId || !product.slug) return;
        try {
          const data = await postCartRequest(`/shop/cart/add/${product.slug}/`, {
            variant_id: variantId,
            quantity: this.qty,
          });
          if (data.ok) {
            const bodyData = Alpine.$data(document.body);
            if (bodyData && bodyData.applyCartResponse) {
              bodyData.applyCartResponse(data);
              bodyData.openCart();
            }
            return;
          }
          alert(data.error || "خطا در افزودن به سبد");
        } catch (e) {
          alert("خطا در اتصال به سرور");
        }
      },
    };
  });
});
