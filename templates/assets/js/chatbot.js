async function chat(message) {

    try {
        const response = await fetch(`${window.location.protocol}//${window.location.host}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                user: ''
            })
        });

        const responseData = await response.json();
        return responseData.response;
    } catch (error) {
        console.error("Error:", error);
        return "Error in processing request";
    }
}
