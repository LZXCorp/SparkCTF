(() => {
  'use strict';

  const logoutForm = document.getElementById('logout-form');
  const consoleRoot = document.getElementById('console-root');
  const statusBar = document.getElementById('global-status');
  const PASSKEY_UUID = consoleRoot?.dataset?.passkeyUuid || '';

  if (logoutForm) {
    logoutForm.addEventListener('submit', (event) => {
      event.preventDefault();
      fetch('/logout', { method: 'POST' })
        .catch(() => null)
        .finally(() => {
          window.location.href = '/';
        });
    });
  }

  if (!consoleRoot) {
    return;
  }

  const panels = {
    login: document.getElementById('login-panel'),
    passkey: document.getElementById('passkey-panel'),
    omega: document.getElementById('omega-panel'),
    result: document.getElementById('result-panel'),
  };

  const loginForm = document.getElementById('login-form');
  const passkeyTrigger = document.getElementById('passkey-trigger');
  const pinSwitch = document.getElementById('pin-switch');
  const fallbackForm = document.getElementById('fallback-form');
  const copyButton = document.getElementById('copy-token');
  const jwtOutput = document.getElementById('jwt-output');
  const flag2Banner = document.getElementById('flag2-banner');
  const loginFeedback = document.getElementById('login-feedback');
  const passkeyFeedback = document.getElementById('passkey-feedback');
  const pinFeedback = document.getElementById('pin-feedback');

  if (!loginForm || !passkeyTrigger || !fallbackForm || !copyButton || !pinSwitch) {
    return;
  }

  let passkeyBusy = false;

  const updateStatus = (message, stateClass = '') => {
    if (!statusBar) {
      return;
    }
    statusBar.textContent = message;
    statusBar.className = `status ${stateClass}`.trim();
  };

  const togglePanel = (panelKey) => {
    Object.entries(panels).forEach(([key, element]) => {
      if (!element) {
        return;
      }
      if (key === panelKey) {
        element.classList.remove('hidden');
        element.classList.add('active');
      } else {
        element.classList.add('hidden');
        element.classList.remove('active');
      }
    });
  };

  const postJSON = (url, body = {}) =>
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).then(async (res) => {
      let data = {};
      try {
        data = await res.json();
      } catch (err) {
        // ignore parse failures so status codes propagate
      }
      return { status: res.status, body: data };
    });

  const showPinSwitch = (message) => {
    passkeyFeedback.textContent = message || 'Alternate vector authorized.';
    updateStatus('Hardware path exhausted. Alternate method available.', 'ok');
    pinSwitch.classList.remove('hidden');
  };

  const applyPasskeyResponse = (result) => {
    if (!result || !result.body) {
      return false;
    }
    const { status, body } = result;
    if (body.status === 'retry') {
      const retryMessage = body.message || 'Authenticator rejected the signature.';
      passkeyFeedback.textContent = retryMessage;
      updateStatus('Authenticator mismatch.', 'warn');
      return true;
    }
    if (body.status === 'alt') {
      showPinSwitch(body.message);
      return true;
    }
    if (status !== 200) {
      passkeyFeedback.textContent = body.error || 'unexpected response';
      updateStatus('Unexpected authenticator response.', 'error');
      return true;
    }
    return false;
  };

  const notifyPasskeyCancellation = async (reason) => {
    try {
      const result = await postJSON('/passkey/cancel', { reason });
      applyPasskeyResponse(result);
    } catch (err) {
      // if cancellation reporting fails, we still keep local messaging
    }
  };

  const base64urlToArrayBuffer = (base64url) => {
    const padding = '='.repeat((4 - (base64url.length % 4)) % 4);
    const base64 = (base64url + padding).replace(/-/g, '+').replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray.buffer;
  };

  const arrayBufferToBase64url = (buffer) => {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    bytes.forEach((b) => {
      binary += String.fromCharCode(b);
    });
    return window.btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  };

  const toAssertionOptions = (options) => ({
    challenge: base64urlToArrayBuffer(options.challenge),
    rpId: options.rpId,
    timeout: options.timeout,
    userVerification: options.userVerification,
    allowCredentials: (options.allowCredentials || []).map((cred) => ({
      ...cred,
      id: base64urlToArrayBuffer(cred.id),
    })),
  });

  const serializeAssertion = (credential) => ({
    id: credential.id,
    rawId: arrayBufferToBase64url(credential.rawId),
    type: credential.type,
    response: {
      authenticatorData: arrayBufferToBase64url(credential.response.authenticatorData),
      clientDataJSON: arrayBufferToBase64url(credential.response.clientDataJSON),
      signature: credential.response.signature ? arrayBufferToBase64url(credential.response.signature) : null,
      userHandle: credential.response.userHandle ? arrayBufferToBase64url(credential.response.userHandle) : null,
    },
    fingerprint: PASSKEY_UUID,
  });

  const invokeAuthenticator = async () => {
    const { status, body } = await postJSON('/passkey/assert/options');
    if (status !== 200 || !body.options) {
      throw new Error(body.error || 'challenge failure');
    }
    const publicKey = toAssertionOptions(body.options);
    const credential = await navigator.credentials.get({ publicKey });
    const serialized = serializeAssertion(credential);
    return postJSON('/passkey/assert', { assertion: serialized });
  };

  togglePanel('login');

  loginForm.addEventListener('submit', (event) => {
    event.preventDefault();
    loginFeedback.textContent = '';
    passkeyFeedback.textContent = '';

    const formData = new FormData(loginForm);
    const username = formData.get('username')?.toString().trim();
    const password = formData.get('password')?.toString() || '';

    postJSON('/login', { username, password })
      .then(({ status, body }) => {
        if (status === 200) {
          updateStatus('Node alpha synchronized. Prepare the hardware channel.', 'ok');
          togglePanel('passkey');
          panels.login?.classList.remove('active');
        } else {
          loginFeedback.textContent = body.error || 'credential rejection';
          updateStatus('Directory handshake failed.', 'error');
        }
      })
      .catch(() => {
        loginFeedback.textContent = 'transport fault';
        updateStatus('Transport failure detected.', 'error');
      });
  });

  passkeyTrigger.addEventListener('click', async () => {
    if (passkeyBusy) {
      return;
    }
    if (!window.PublicKeyCredential) {
      passkeyFeedback.textContent = 'Passkey APIs unavailable in this environment.';
      updateStatus('Platform authenticator unsupported.', 'error');
      return;
    }

    passkeyBusy = true;
    passkeyFeedback.textContent = '';
    updateStatus('Awaiting authenticator confirmation...', 'warn');

    try {
      const { status, body } = await invokeAuthenticator();

      const handled = applyPasskeyResponse({ status, body });
      if (!handled) {
        passkeyFeedback.textContent = body?.message || 'unexpected response';
        updateStatus('Unexpected authenticator response.', 'error');
      }
    } catch (err) {
      const message = err?.message === 'unsupported'
        ? 'Browser denied WebAuthn API.'
        : 'Authenticator dismissed the prompt.';
      passkeyFeedback.textContent = message;
      updateStatus('Authenticator cancelled.', 'error');
      await notifyPasskeyCancellation(message);
    } finally {
      passkeyBusy = false;
    }
  });

  pinSwitch.addEventListener('click', () => {
    pinSwitch.classList.add('hidden');
    fallbackForm.classList.remove('hidden');
    togglePanel('omega');
    updateStatus('Fallback channel armed. Provide channel key.', 'warn');
  });

  fallbackForm.addEventListener('submit', (event) => {
    event.preventDefault();
    pinFeedback.textContent = '';

    const secret = (event.target['fallback-secret'].value || '').trim();
    if (!secret) {
      pinFeedback.textContent = 'enter the channel key';
      return;
    }

    postJSON('/pin', { secret })
      .then(({ status, body }) => {
        if (status === 200 && body.token) {
          updateStatus('Node gamma accepted. Session established.', 'ok');
          if (body.flag) {
            flag2Banner.textContent = `Flag 2: ${body.flag}`;
            flag2Banner.classList.remove('hidden');
          }
          window.location.href = body.redirect || '/';
        } else {
          pinFeedback.textContent = body.error || 'invalid entry';
          updateStatus('Fallback secret rejected.', 'error');
        }
      })
      .catch(() => {
        pinFeedback.textContent = 'transport fault';
        updateStatus('Transport failure detected.', 'error');
      });
  });

  copyButton.addEventListener('click', async () => {
    if (!jwtOutput.value) {
      return;
    }
    try {
      await navigator.clipboard.writeText(jwtOutput.value);
      updateStatus('Token copied to clipboard.', 'ok');
    } catch (err) {
      updateStatus('Clipboard unavailable. Copy manually.', 'warn');
    }
  });
})();
