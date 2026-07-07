document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('generator-form');

    if (form) {
        form.addEventListener('submit', function (e) {
            const lengthInput = document.querySelector('input[name="length"]');
            const val = parseInt(lengthInput.value, 10) || 0;

            if (val < 6) {
                e.preventDefault();
                lengthInput.value = 6;
                showToast('Minimum length: 6 characters', { type: 'error' });
                lengthInput.focus();
            }
        });
    }

});

function copyPassword() {
    let password = document.getElementById("password");

    if (!password) return;

    password.select();
    password.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(password.value);
    showToast("Password Copied Successfully!", { type: 'info' });

}

// Toast helper
function showToast(message, opts = {}) {
    const { timeout = 1500, type = 'info' } = opts;
    let toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.remove('error', 'info');
    toast.classList.add(type === 'error' ? 'error' : 'info');
    toast.classList.add('show');
    clearTimeout(toast._hideTimer);
    toast._hideTimer = setTimeout(() => {
        toast.classList.remove('show');
    }, timeout);
}

// Enforce min/max on length input while interacting (no snapping below min)
document.addEventListener('DOMContentLoaded', function() {
    const lengthInput = document.querySelector('input[name="length"]');
    if (!lengthInput) return;

    const min = parseInt(lengthInput.min, 10);
    const max = parseInt(lengthInput.max, 10) || 50;
    const requiredMin = 6;

    lengthInput.addEventListener('input', function () {
        let cur = parseInt(lengthInput.value, 10);
        if (isNaN(cur)) {
            lengthInput.value = min !== undefined ? min : 0;
            return;
        }

        if (cur > max) {
            lengthInput.value = max;
            showToast('Maximum length is ' + max, { type: 'error' });
            return;
        }

        if (cur < 0) {
            lengthInput.value = 0;
            showToast('Length cannot be negative', { type: 'error' });
            return;
        }

        if (cur > 0 && cur < requiredMin) {
            showToast('Minimum length: ' + requiredMin + ' characters', { type: 'error' });
        }
    });

    // If server returned an error or success message, show it via toast
    const serverError = document.getElementById('server-error');
    if (serverError) {
        const msg = serverError.getAttribute('data-error');
        if (msg) showToast(msg, { type: 'error' });
    }

    const serverSuccess = document.getElementById('server-success');
    if (serverSuccess) {
        const msg = serverSuccess.getAttribute('data-success');
        if (msg) showToast(msg, { type: 'info' });
    }
});
