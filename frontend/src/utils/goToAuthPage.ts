export const goToAuthPage = () => {
    function formDeserialize(form, data) {
        const entries = Object.entries(data);

        for (const [key, val] of entries) {
            const input = form.elements[key];
            input.value = val;
        }
    }

    const form = document.querySelector('form#login')!;
    let data = {
        client_id: 'corp',
        response_type: 'code',
        scope: 'openid profile',
        redirect_uri: window.location.origin + '/',
    };
    formDeserialize(form, data);
    form.submit();
};
