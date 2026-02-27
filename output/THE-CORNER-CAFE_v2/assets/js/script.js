'use strict';

document.addEventListener('DOMContentLoaded', init);

function init() {
  initNavDrawer();
  initSmoothScroll();
  initReveal();
  initMenuTabs();
  initAccordion();
  initContactForm();
  initHeaderScroll();
}

// ─────────────────────────────────────────────
// 1. ハンバーガーメニュー（ドロワー）
// ─────────────────────────────────────────────
function initNavDrawer() {
  const hamburger = document.querySelector('.c-hamburger');
  const closeBtn  = document.querySelector('.c-hamburger--close');
  const drawer    = document.getElementById('nav-drawer');
  const overlay   = document.querySelector('.p-nav-overlay');

  // 必要な要素がなければスキップ
  if (!hamburger || !drawer) return;

  /** ドロワーを開く */
  function openDrawer() {
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    overlay?.classList.add('is-active');
    hamburger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  /** ドロワーを閉じる */
  function closeDrawer() {
    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    overlay?.classList.remove('is-active');
    hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  // ハンバーガーボタンで開閉トグル
  hamburger.addEventListener('click', () => {
    const isOpen = drawer.classList.contains('is-open');
    isOpen ? closeDrawer() : openDrawer();
  });

  // 閉じるボタン
  closeBtn?.addEventListener('click', closeDrawer);

  // オーバーレイクリックで閉じる
  overlay?.addEventListener('click', closeDrawer);

  // ドロワー内リンクをクリックしたら閉じる
  drawer.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeDrawer);
  });

  // Escape キーで閉じる
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
      closeDrawer();
      hamburger.focus(); // フォーカスをトリガーに戻す
    }
  });
}

// ─────────────────────────────────────────────
// 2. スムーズスクロール（ナビリンク）
// ─────────────────────────────────────────────
function initSmoothScroll() {
  const HEADER_HEIGHT = 64; // px: ヘッダーの固定高さ

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const hash = anchor.getAttribute('href');

      // ページ内リンクでない場合はスキップ
      if (!hash || hash === '#') return;

      const target = document.querySelector(hash);
      if (!target) return;

      e.preventDefault();

      // scrollMarginTop を設定してからスクロール
      target.style.scrollMarginTop = HEADER_HEIGHT + 'px';

      target.scrollIntoView({ behavior: 'smooth', block: 'start' });

      // URL ハッシュを更新（スクロール位置は変えない）
      history.pushState(null, '', hash);

      // フォーカスをターゲットに移動（アクセシビリティ）
      if (!target.hasAttribute('tabindex')) {
        target.setAttribute('tabindex', '-1');
      }
      target.focus({ preventScroll: true });
    });
  });
}

// ─────────────────────────────────────────────
// 3. スクロールリビール（IntersectionObserver）
// ─────────────────────────────────────────────
function initReveal() {
  const revealItems = document.querySelectorAll('.reveal');
  if (!revealItems.length) return;

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          // 一度表示したら監視を解除
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px',
    }
  );

  revealItems.forEach(item => observer.observe(item));
}

// ─────────────────────────────────────────────
// 4. メニュータブ（コーヒー / スイーツ）
// Fix 1: セレクターを HTML の実装に合わせて修正
//   タブボタン: data-tab="coffee" / data-tab="sweets"
//   パネル: class="p-menu__grid" data-category="coffee" / data-category="sweets"
// ─────────────────────────────────────────────
function initMenuTabs() {
  const tabs   = document.querySelectorAll('.p-menu__tab');
  // Fix 1: .p-menu__panel ではなく .p-menu__grid[data-category] を使う
  const panels = document.querySelectorAll('.p-menu__grid[data-category]');

  if (!tabs.length || !panels.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetKey = tab.dataset.tab;

      // すべてのタブを非アクティブにする
      tabs.forEach(t => {
        t.classList.remove('is-active');
        t.setAttribute('aria-selected', 'false');
      });

      // すべてのパネルを非表示にする
      panels.forEach(panel => {
        panel.setAttribute('hidden', '');
      });

      // クリックされたタブをアクティブにする
      tab.classList.add('is-active');
      tab.setAttribute('aria-selected', 'true');

      // Fix 1: data-category 属性で対応するパネルを探す
      panels.forEach(panel => {
        if (panel.dataset.category === targetKey) {
          panel.removeAttribute('hidden');
        }
      });
    });
  });
}

// ─────────────────────────────────────────────
// 5. FAQ アコーディオン
// ─────────────────────────────────────────────
function initAccordion() {
  const accordions = document.querySelectorAll('.c-accordion');
  if (!accordions.length) return;

  accordions.forEach(accordion => {
    const trigger = accordion.querySelector('.c-accordion__trigger');
    const panelId = trigger?.getAttribute('aria-controls');
    const panel   = panelId ? document.getElementById(panelId) : null;

    if (!trigger || !panel) return;

    // Escape キーでフォーカスをトリガーに戻す
    panel.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        trigger.focus();
      }
    });

    trigger.addEventListener('click', () => {
      const isExpanded = trigger.getAttribute('aria-expanded') === 'true';

      if (isExpanded) {
        // 閉じる
        trigger.setAttribute('aria-expanded', 'false');
        panel.hidden = true;
      } else {
        // 開く（他のアコーディオンは閉じない：複数同時展開 OK）
        trigger.setAttribute('aria-expanded', 'true');
        panel.hidden = false;
      }
    });
  });
}

// ─────────────────────────────────────────────
// 6. お問い合わせフォームバリデーション + 送信
// ─────────────────────────────────────────────
function initContactForm() {
  // フォームがなければスキップ
  const form = document.getElementById('contact-form')
    ?? document.querySelector('.p-contact__form');
  if (!form) return;

  const submitBtn    = form.querySelector('[type="submit"]');
  const successMsg   = document.getElementById('form-success');
  const errorMsg     = document.getElementById('form-error');
  const nameField    = form.querySelector('[name="name"]');
  const emailField   = form.querySelector('[name="email"]');
  const messageField = form.querySelector('[name="message"]');
  const honeypot     = form.querySelector('[name="website"]');

  const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  /** フィールドのエラーを表示する */
  function showFieldError(field, message) {
    field.classList.add('is-error');
    field.setAttribute('aria-invalid', 'true');

    // 既存エラーメッセージを削除してから追加
    const existing = field.parentElement.querySelector('.form-error, .p-contact__field-error');
    if (existing) existing.remove();

    const errorEl = document.createElement('p');
    errorEl.className = 'p-contact__field-error';
    errorEl.setAttribute('role', 'alert');
    errorEl.setAttribute('aria-live', 'polite');
    // textContent を使用して XSS を防ぐ
    errorEl.textContent = message;
    field.parentElement.appendChild(errorEl);
  }

  /** フィールドのエラーをクリアする */
  function clearFieldError(field) {
    field.classList.remove('is-error');
    field.removeAttribute('aria-invalid');
    const existing = field.parentElement.querySelector('.form-error, .p-contact__field-error');
    if (existing) existing.remove();
  }

  /** フォーム全体をバリデーションして有効かどうかを返す */
  function validateForm() {
    let isValid = true;

    // name チェック
    if (nameField) {
      const nameVal = nameField.value.trim();
      if (!nameVal || nameVal.length < 1 || nameVal.length > 100) {
        showFieldError(nameField, 'お名前を1〜100文字で入力してください。');
        isValid = false;
      } else {
        clearFieldError(nameField);
      }
    }

    // email チェック
    if (emailField) {
      const emailVal = emailField.value.trim();
      if (!emailVal || !EMAIL_REGEX.test(emailVal)) {
        showFieldError(emailField, '有効なメールアドレスを入力してください。');
        isValid = false;
      } else {
        clearFieldError(emailField);
      }
    }

    // message チェック
    if (messageField) {
      const msgVal = messageField.value.trim();
      if (!msgVal || msgVal.length < 1 || msgVal.length > 2000) {
        showFieldError(messageField, 'お問い合わせ内容を1〜2000文字で入力してください。');
        isValid = false;
      } else {
        clearFieldError(messageField);
      }
    }

    return isValid;
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();

    // Honeypot チェック: website フィールドが埋まっていたらサイレントキャンセル
    if (honeypot && honeypot.value.trim() !== '') {
      // ボットの可能性: 何も通知せず静かに終了
      return;
    }

    // バリデーション
    if (!validateForm()) return;

    // 送信中状態に変更（二重送信防止）
    const originalBtnText = submitBtn?.textContent ?? '送信する';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = '送信中...';
    }

    // グローバルエラー表示をリセット
    if (errorMsg) errorMsg.hidden = true;

    try {
      const formData = new FormData(form);

      const response = await fetch(form.action || 'php/form_handler.php', {
        method: 'POST',
        body: formData,
      });

      // レスポンスが JSON でない場合も考慮
      let result;
      try {
        result = await response.json();
      } catch {
        result = { success: false, message: 'サーバーエラーが発生しました。' };
      }

      if (response.ok && result.success) {
        // 成功: フォームを非表示にして成功メッセージを表示
        form.hidden = true;
        if (successMsg) {
          successMsg.hidden = false;
          successMsg.focus();
        }
      } else {
        // 失敗: エラーメッセージを表示してボタンを復元
        if (errorMsg) {
          errorMsg.hidden = false;
          // エラーメッセージの中身を安全に更新
          const msgEl = errorMsg.querySelector('[data-message]') ?? errorMsg;
          msgEl.textContent = result.message || '送信に失敗しました。もう一度お試しください。';
          errorMsg.focus();
        }
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = originalBtnText;
        }
      }
    } catch {
      // ネットワークエラーなど
      if (errorMsg) {
        errorMsg.hidden = false;
        errorMsg.focus();
      }
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
      }
    }
  });

  // リアルタイムバリデーション: フォーカスが外れたときにチェック
  [nameField, emailField, messageField].forEach(field => {
    if (!field) return;
    field.addEventListener('blur', () => {
      // 一度もエラーが出たフィールドだけリアルタイム検証
      if (field.classList.contains('is-error')) {
        validateForm();
      }
    });
  });
}

// ─────────────────────────────────────────────
// 7. ヘッダースクロール挙動
// ─────────────────────────────────────────────
function initHeaderScroll() {
  const header = document.querySelector('.p-header');
  if (!header) return;

  const SCROLL_THRESHOLD = 80; // px

  function updateHeader() {
    if (window.scrollY > SCROLL_THRESHOLD) {
      header.classList.add('is-scrolled');
    } else {
      header.classList.remove('is-scrolled');
    }
  }

  // 初回実行（リロード時にすでにスクロールされている場合に対応）
  updateHeader();

  window.addEventListener('scroll', updateHeader, { passive: true });
}
