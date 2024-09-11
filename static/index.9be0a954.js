async function chat(message) {
    try {
        const response = await fetch('/chat', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                user: "User"
            })
        });
        const responseData = await response.json();
        return responseData.response;
    } catch (error) {
        console.error("Error:", error);
        return "Error in processing request";
    }
}

//# sourceMappingURL=index.9be0a954.js.map
