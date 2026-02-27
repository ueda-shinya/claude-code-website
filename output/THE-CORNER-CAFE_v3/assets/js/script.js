'use strict';

// ===================================================================
// UTILITY FUNCTIONS
// ===================================================================

/**
 * ヘッダーの高さを取得（レスポンシブ対応）
 */
function getHeaderHeight() {
  const header = document.getElementById('header');
  return header ? header.offsetHeight : 64;
}

// ===================================================================
// 1. HAMBURGER MENU
// ===================================================================
(function initHamburger() {
  const hamburger = document.getElementById('js-hamburger');
  const nav = document.getElementById('js-nav');
  if (!hamburger || !nav) return;

  function openNav() {
    nav.classList.add('is-open');
    hamburger.classList.add('is-open');
    hamburger.setAttribute('aria-expanded', 'true');
    hamburger.setAttribute('aria-label', 'メニューを閉じる');
    document.body.classList.add('is-nav-open');
  }

  function closeNav() {
    nav.classList.remove('is-open');
    hamburger.classList.remove('is-open');
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.setAttribute('aria-label', 'メニューを開く');
    document.body.classList.remove('is-nav-open');
  }

  hamburger.addEventListener('click', function () {
    const isOpen = hamburger.classList.contains('is-open');
    if (isOpen) { closeNav(); } else { openNav(); }
  });

  // ナビリンク クリックで閉じる
  nav.querySelectorAll('.c-nav__link').forEach(function (link) {
    link.addEventListener('click', closeNav);
  });

  // 768px以上でリサイズしたら強制クローズ
  window.addEventListener('resize', function () {
    if (window.innerWidth >= 768) { closeNav(); }
  });
})();

// ===================================================================
// 2. SMOOTH SCROLL
// ===================================================================
(function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"], .js-scroll-to').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const headerHeight = getHeaderHeight();
      const targetTop = target.getBoundingClientRect().top + window.pageYOffset - headerHeight - 8;
      window.scrollTo({ top: targetTop, behavior: 'smooth' });
    });
  });
})();

// ===================================================================
// 3. HEADER SCROLL EFFECT
// ===================================================================
(function initHeaderScroll() {
  const header = document.getElementById('header');
  if (!header) return;
  let ticking = false;

  function updateHeader() {
    if (window.scrollY > 50) {
      header.classList.add('is-scrolled');
    } else {
      header.classList.remove('is-scrolled');
    }
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(updateHeader);
      ticking = true;
    }
  }, { passive: true });
})();

// ===================================================================
// 4. SCROLL REVEAL
// ===================================================================
(function initScrollReveal() {
  if (!('IntersectionObserver' in window)) {
    // フォールバック: 全要素を即表示
    document.querySelectorAll('.js-reveal, .js-reveal-stagger').forEach(function (el) {
      el.classList.add('is-visible');
    });
    return;
  }

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.js-reveal, .js-reveal-stagger').forEach(function (el) {
    observer.observe(el);
  });
})();

// ===================================================================
// 5. COUNTER ANIMATION
// ===================================================================
(function initCounters() {
  const counters = document.querySelectorAll('.js-stats-counter[data-target]');
  if (!counters.length) return;

  function easeOutQuad(t) { return t * (2 - t); }

  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target'), 10);
    if (isNaN(target)) return;
    const duration = 1500;
    const start = performance.now();

    function step(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutQuad(progress);
      el.textContent = Math.floor(eased * target).toString();
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target.toString();
      }
    }
    requestAnimationFrame(step);
  }

  if (!('IntersectionObserver' in window)) {
    counters.forEach(animateCounter);
    return;
  }

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(function (counter) { observer.observe(counter); });
})();

// ===================================================================
// 6. TAB NAVIGATION
// ===================================================================
(function initTabs() {
  const tabs = document.querySelectorAll('.js-tab');
  const panels = document.querySelectorAll('.p-menu__panel');
  if (!tabs.length) return;

  function activateTab(tab) {
    // 全タブ無効化
    tabs.forEach(function (t) {
      t.classList.remove('is-active');
      t.setAttribute('aria-selected', 'false');
    });
    // 全パネル非表示
    panels.forEach(function (p) { p.classList.remove('is-active'); });
    // 対象タブ・パネルを有効化
    tab.classList.add('is-active');
    tab.setAttribute('aria-selected', 'true');
    const targetId = 'panel-' + tab.getAttribute('data-target');
    const panel = document.getElementById(targetId);
    if (panel) { panel.classList.add('is-active'); }
  }

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () { activateTab(this); });
    // キーボード操作
    tab.addEventListener('keydown', function (e) {
      const tabArray = Array.from(tabs);
      const index = tabArray.indexOf(this);
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        const next = tabArray[(index + 1) % tabArray.length];
        next.focus();
        activateTab(next);
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        const prev = tabArray[(index - 1 + tabArray.length) % tabArray.length];
        prev.focus();
        activateTab(prev);
      }
    });
  });
})();

// ===================================================================
// 7. ACCORDION
// ===================================================================
(function initAccordion() {
  const accordions = document.querySelectorAll('.js-accordion');
  if (!accordions.length) return;

  accordions.forEach(function (item) {
    const trigger = item.querySelector('.c-accordion__trigger');
    if (!trigger) return;

    trigger.addEventListener('click', function () {
      const isOpen = item.classList.contains('is-open');

      // 全て閉じる
      accordions.forEach(function (other) {
        other.classList.remove('is-open');
        const otherTrigger = other.querySelector('.c-accordion__trigger');
        if (otherTrigger) { otherTrigger.setAttribute('aria-expanded', 'false'); }
      });

      // クリックしたものが閉じていたら開く
      if (!isOpen) {
        item.classList.add('is-open');
        trigger.setAttribute('aria-expanded', 'true');
      }
    });
  });
})();

// ===================================================================
// 8 & 9. FORM VALIDATION & SUBMISSION
// ===================================================================
(function initForm() {
  const form = document.querySelector('.js-contact-form');
  if (!form) return;

  const submitBtn = form.querySelector('.js-submit-btn');
  const successEl = document.getElementById('form-success');
  const errorEl = document.getElementById('form-error');
  let isSubmitting = false;

  const errorMessages = {
    name: {
      empty: 'お名前を入力してください',
      tooLong: '50文字以内で入力してください'
    },
    email: {
      empty: 'メールアドレスを入力してください',
      invalid: '正しいメールアドレスの形式で入力してください',
      tooLong: '254文字以内で入力してください'
    },
    inquiry_type: {
      empty: 'お問い合わせの種類を選択してください'
    },
    message: {
      empty: 'メッセージを入力してください',
      tooLong: '1000文字以内でご入力ください'
    },
    tel: {
      invalid: '電話番号はハイフンあり・なしどちらでも入力できます（例：090-1234-5678）'
    }
  };

  function getErrorEl(field) {
    const describedBy = field.getAttribute('aria-describedby');
    if (describedBy) { return document.getElementById(describedBy); }
    return null;
  }

  function setError(field, message) {
    const errEl = getErrorEl(field);
    field.classList.add('is-error');
    if (errEl) {
      errEl.textContent = message; // XSS防止: textContent を使用
      errEl.classList.add('is-visible');
    }
  }

  function clearError(field) {
    const errEl = getErrorEl(field);
    field.classList.remove('is-error');
    if (errEl) {
      errEl.textContent = '';
      errEl.classList.remove('is-visible');
    }
  }

  function validateField(field) {
    const value = field.value.trim();
    const id = field.id;
    clearError(field);

    if (field.required && !value) {
      const msg = (errorMessages[id] && errorMessages[id].empty) || '必須項目です';
      setError(field, msg);
      return false;
    }

    if (id === 'name' && value.length > 50) {
      setError(field, errorMessages.name.tooLong);
      return false;
    }

    if (id === 'email' && value) {
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        setError(field, errorMessages.email.invalid);
        return false;
      }
      if (value.length > 254) {
        setError(field, errorMessages.email.tooLong);
        return false;
      }
    }

    if (id === 'tel' && value) {
      if (!/^[\d\-+\s()]+$/.test(value)) {
        setError(field, errorMessages.tel.invalid);
        return false;
      }
    }

    if (id === 'message' && value.length > 1000) {
      setError(field, errorMessages.message.tooLong);
      return false;
    }

    return true;
  }

  // リアルタイムバリデーション（blur時）
  const fields = form.querySelectorAll('.c-form__input');
  fields.forEach(function (field) {
    field.addEventListener('blur', function () { validateField(this); });
    field.addEventListener('input', function () {
      if (this.classList.contains('is-error')) { validateField(this); }
    });
  });

  // フォーム送信
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (isSubmitting) return;

    // Honeypot チェック
    const honeypot = form.querySelector('input[name="website"]');
    if (honeypot && honeypot.value) { return; }

    // 全フィールドバリデーション
    let isValid = true;
    let firstErrorField = null;
    fields.forEach(function (field) {
      if (!validateField(field)) {
        isValid = false;
        if (!firstErrorField) { firstErrorField = field; }
      }
    });

    // プライバシー同意チェック
    const privacy = form.querySelector('input[name="privacy"]');
    if (privacy && !privacy.checked) {
      isValid = false;
      if (!firstErrorField) { firstErrorField = privacy; }
    }

    if (!isValid) {
      if (firstErrorField) {
        const headerHeight = getHeaderHeight();
        const top = firstErrorField.getBoundingClientRect().top + window.pageYOffset - headerHeight - 20;
        window.scrollTo({ top: top, behavior: 'smooth' });
        setTimeout(function () { firstErrorField.focus(); }, 500);
      }
      return;
    }

    // 送信処理
    isSubmitting = true;
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = '送信しています...';
    }

    const formData = new FormData(form);

    fetch(form.getAttribute('action'), {
      method: 'POST',
      body: formData
    })
      .then(function (response) {
        if (!response.ok) { throw new Error('Network error: ' + response.status); }
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          form.style.opacity = '0';
          form.style.transform = 'translateY(8px)';
          form.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
          setTimeout(function () {
            form.style.display = 'none';
            if (successEl) {
              successEl.style.display = 'block';
              requestAnimationFrame(function () {
                successEl.classList.add('is-visible');
              });
            }
            if (submitBtn) { submitBtn.textContent = '送信しました'; }
          }, 300);
        } else {
          throw new Error(data.message || 'Server error');
        }
      })
      .catch(function () {
        if (errorEl) {
          errorEl.style.display = 'block';
          requestAnimationFrame(function () {
            errorEl.classList.add('is-visible');
          });
        }
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = '送信する';
        }
        isSubmitting = false;
      });
  });
})();

// ===================================================================
// 10. PRIVACY POLICY MODAL
// ===================================================================
(function initModal() {
  const modal = document.getElementById('modal-privacy');
  if (!modal) return;

  const openBtn = document.querySelector('.js-privacy-open');
  const closeBtns = modal.querySelectorAll('.js-modal-close');
  let lastFocused = null;

  function openModal() {
    lastFocused = document.activeElement;
    modal.removeAttribute('hidden');
    document.body.classList.add('is-nav-open');
    const closeBtn = modal.querySelector('.c-modal__close');
    if (closeBtn) { closeBtn.focus(); }
  }

  function closeModal() {
    modal.setAttribute('hidden', '');
    document.body.classList.remove('is-nav-open');
    if (lastFocused) { lastFocused.focus(); }
  }

  if (openBtn) { openBtn.addEventListener('click', openModal); }
  closeBtns.forEach(function (btn) { btn.addEventListener('click', closeModal); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hasAttribute('hidden')) { closeModal(); }
  });
})();
