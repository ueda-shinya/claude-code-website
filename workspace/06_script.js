'use strict';

/**
 * THE CORNER CAFE — script.js
 * バニラJS (ES6+) / ライブラリ不使用
 */

document.addEventListener('DOMContentLoaded', () => {

  // ============================================================
  // 1. ハンバーガーメニュー / ドロワー
  // ============================================================

  const hamburger  = document.querySelector('.js-hamburger');
  const drawer     = document.querySelector('#drawer');
  const closeButtons = document.querySelectorAll('.js-drawer-close');

  // オーバーレイ生成
  const overlay = document.createElement('div');
  overlay.className = 'l-drawer-overlay';
  document.body.appendChild(overlay);

  function openDrawer() {
    drawer.classList.add('is-open');
    overlay.classList.add('is-open');
    document.body.classList.add('is-drawer-open');
    if (hamburger) {
      hamburger.classList.add('is-active');
      hamburger.setAttribute('aria-expanded', 'true');
    }
    // フォーカスを閉じるボタンへ
    const closeBtn = drawer.querySelector('.l-drawer__close');
    if (closeBtn) closeBtn.focus();
  }

  function closeDrawer() {
    drawer.classList.remove('is-open');
    overlay.classList.remove('is-open');
    document.body.classList.remove('is-drawer-open');
    if (hamburger) {
      hamburger.classList.remove('is-active');
      hamburger.setAttribute('aria-expanded', 'false');
    }
    if (hamburger) hamburger.focus();
  }

  if (hamburger && drawer) {
    hamburger.addEventListener('click', openDrawer);
    overlay.addEventListener('click', closeDrawer);

    closeButtons.forEach(btn => {
      btn.addEventListener('click', closeDrawer);
    });

    // Escキーで閉じる
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        closeDrawer();
      }
    });
  }

  // ============================================================
  // 2. スムーズスクロール
  // ============================================================

  const header = document.querySelector('.l-header');

  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const hash = link.getAttribute('href');
      if (hash === '#') return;
      const target = document.querySelector(hash);
      if (!target) return;
      e.preventDefault();

      const headerHeight = header ? header.offsetHeight : 0;
      const targetTop = target.getBoundingClientRect().top + window.scrollY - headerHeight - 8;

      window.scrollTo({ top: targetTop, behavior: 'smooth' });
    });
  });

  // ============================================================
  // 3. ヘッダー スクロール変化（is-scrolled）
  // ============================================================

  if (header) {
    const onScroll = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 60);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ============================================================
  // 4. スクロールリビール（js-reveal → is-visible）
  // ============================================================

  const revealElements = document.querySelectorAll('.js-reveal');

  if (revealElements.length > 0 && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const delay = parseInt(el.dataset.delay || '0', 10);
        setTimeout(() => {
          el.classList.add('is-visible');
        }, delay);
        revealObserver.unobserve(el);
      });
    }, { threshold: 0.15 });

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    // IntersectionObserver非対応ブラウザは即表示
    revealElements.forEach(el => el.classList.add('is-visible'));
  }

  // ============================================================
  // 5. 実績カウントアップ（js-stats-count）
  // ============================================================

  const statsItems = document.querySelectorAll('.js-stats-count');

  function animateCount(el, from, to, duration, suffix) {
    const start = performance.now();
    const update = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // easeOut
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(from + (to - from) * eased);
      el.textContent = current + suffix;
      if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  }

  if (statsItems.length > 0 && 'IntersectionObserver' in window) {
    const statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const item = entry.target;
        const numEl = item.querySelector('[data-count]');
        if (!numEl) return;
        const target = parseInt(numEl.dataset.count, 10);
        const suffix = numEl.dataset.suffix || '';
        animateCount(numEl, 0, target, 1500, suffix);
        statsObserver.unobserve(item);
      });
    }, { threshold: 0.3 });

    statsItems.forEach(item => statsObserver.observe(item));
  }

  // ============================================================
  // 6. メニュータブ（js-menu-tab）
  // ============================================================

  const tabButtons = document.querySelectorAll('.js-menu-tab');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      // 全タブを非アクティブに
      tabButtons.forEach(b => {
        b.classList.remove('is-active');
        b.setAttribute('aria-selected', 'false');
      });

      // クリックしたタブをアクティブに
      btn.classList.add('is-active');
      btn.setAttribute('aria-selected', 'true');

      // 全パネルを非表示
      const panelIds = Array.from(tabButtons).map(b => b.getAttribute('aria-controls'));
      panelIds.forEach(id => {
        const panel = document.getElementById(id);
        if (panel) panel.classList.add('u-hidden');
      });

      // 対応パネルを表示
      const targetId = btn.getAttribute('aria-controls');
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) targetPanel.classList.remove('u-hidden');
    });
  });

  // ============================================================
  // 7. FAQアコーディオン（js-accordion）
  // ============================================================

  const accordionItems = document.querySelectorAll('.js-accordion');

  accordionItems.forEach(item => {
    const btn = item.querySelector('.c-accordion__question');
    if (!btn) return;

    btn.addEventListener('click', () => {
      const isOpen = item.classList.contains('is-open');

      // 他を全て閉じる
      accordionItems.forEach(other => {
        other.classList.remove('is-open');
        const otherBtn = other.querySelector('.c-accordion__question');
        if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
      });

      // クリックしたものをトグル
      if (!isOpen) {
        item.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // ============================================================
  // 8. お問い合わせフォーム
  // ============================================================

  const form = document.querySelector('.js-form');
  if (!form) return;

  const submitBtn = form.querySelector('.js-form-submit');
  const thanksEl  = document.querySelector('.p-contact__thanks');

  // エスケープ（XSS防止）
  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // エラー表示
  function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorEl = document.getElementById(fieldId + '-error');
    if (field) field.classList.add('is-error');
    if (errorEl) errorEl.textContent = message;
  }

  // エラークリア
  function clearError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorEl = document.getElementById(fieldId + '-error');
    if (field) field.classList.remove('is-error');
    if (errorEl) errorEl.textContent = '';
  }

  // 全エラークリア
  function clearAllErrors() {
    ['name', 'email', 'inquiry-type', 'message', 'privacy'].forEach(id => clearError(id));
  }

  // メールアドレス形式チェック
  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // バリデーション
  function validate() {
    clearAllErrors();
    let isValid = true;

    const name     = form.querySelector('#name');
    const email    = form.querySelector('#email');
    const inquType = form.querySelector('#inquiry-type');
    const message  = form.querySelector('#message');
    const privacy  = form.querySelector('#privacy');

    if (!name.value.trim()) {
      showError('name', 'お名前を入力してください。');
      isValid = false;
    } else if (name.value.length > 100) {
      showError('name', 'お名前は100文字以内でご入力ください。');
      isValid = false;
    }

    if (!email.value.trim()) {
      showError('email', 'メールアドレスを入力してください。');
      isValid = false;
    } else if (!isValidEmail(email.value)) {
      showError('email', '正しい形式のメールアドレスを入力してください。（例: example@mail.com）');
      isValid = false;
    }

    if (!inquType.value) {
      showError('inquiry-type', 'お問い合わせの種類を選択してください。');
      isValid = false;
    }

    if (!message.value.trim()) {
      showError('message', 'お問い合わせ内容を入力してください。');
      isValid = false;
    } else if (message.value.length > 2000) {
      showError('message', 'お問い合わせ内容は2000文字以内でご入力ください。');
      isValid = false;
    }

    if (!privacy.checked) {
      showError('privacy', 'プライバシーポリシーへの同意が必要です。');
      isValid = false;
    }

    return isValid;
  }

  // リアルタイムエラークリア
  ['name', 'email', 'inquiry-type', 'message'].forEach(id => {
    const el = form.querySelector('#' + id);
    if (el) {
      el.addEventListener('input', () => clearError(id));
      el.addEventListener('change', () => clearError(id));
    }
  });

  const privacyEl = form.querySelector('#privacy');
  if (privacyEl) privacyEl.addEventListener('change', () => clearError('privacy'));

  // フォーム送信
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Honeypot チェック
    const honeypot = form.querySelector('#website');
    if (honeypot && honeypot.value) return;

    if (!validate()) {
      // 最初のエラーフィールドへフォーカス
      const firstError = form.querySelector('.is-error');
      if (firstError) firstError.focus();
      return;
    }

    // 二重送信防止
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.classList.add('is-disabled');
      submitBtn.textContent = '送信中...';
    }

    try {
      const formData = new FormData(form);
      const response = await fetch(form.action, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Server error: ' + response.status);

      // 成功
      const formWrapper = form.closest('.p-contact__form') || form.parentElement;
      form.classList.add('u-hidden');
      if (thanksEl) {
        thanksEl.classList.remove('u-hidden');
        thanksEl.focus();
      }

    } catch (err) {
      console.error('Form submit error:', err);
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('is-disabled');
        submitBtn.textContent = '送信する';
      }
      // サーバーエラーメッセージをフォーム上部に表示
      let serverError = form.querySelector('.c-form__server-error');
      if (!serverError) {
        serverError = document.createElement('p');
        serverError.className = 'c-form__error c-form__server-error';
        form.prepend(serverError);
      }
      serverError.textContent = '送信に失敗しました。しばらく時間をおいて再度お試しください。';
    }
  });

});
