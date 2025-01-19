document.addEventListener('DOMContentLoaded', function ()
{
    function togglePasswordVisibility(toggleClass, passwordFieldName)
    {
        document.querySelectorAll(toggleClass).forEach(function(icon)
        {
            icon.addEventListener('click', function()
            {
                const passwordInput = document.querySelector(`input[name="${passwordFieldName}"]`);
                if (passwordInput)
                {
                    if (passwordInput.type === "password")
                    {
                        passwordInput.type = "text";
                        icon.classList.remove('fa-eye');
                        icon.classList.add('fa-eye-slash');
                    }
                    else
                    {
                        passwordInput.type = "password";
                        icon.classList.remove('fa-eye-slash');
                        icon.classList.add('fa-eye');
                    }
                }
            });
        });
    }
    togglePasswordVisibility('.togglePassword', 'password');
    togglePasswordVisibility('.toggleRepeatPassword', 'repeat_password');
    togglePasswordVisibility('.toggleLoginPassword', 'password');
});