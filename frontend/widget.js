const form = document.getElementById("membership-form");
const message = document.getElementById("form-message");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(form);

    const data = {
        visitor_name: formData.get("visitor_name"),
        request_type: "membership_inquiry",
        email: formData.get("email"),
        phone: formData.get("phone"),
        membership_id: formData.get("membership_id"),
        room_number: formData.get("room_number"),
        message: formData.get("message")
    };

    message.textContent = "Submitting...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/submissions/5",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Submission failed");
        }

        message.textContent = "Form submitted successfully!";
        form.reset();

    } catch (error) {
        console.error(error);
        message.textContent = "Submission failed. Please try again.";
    }
});