async function tryOnClothes(userFile, clothImageUrl, storeId) {
    try {
        // Fetch the cloth image as a Blob
        const clothBlob = await fetch(clothImageUrl).then(res => res.blob());

        // Create FormData
        const formData = new FormData();
        formData.append("store_id", storeId);
        formData.append("user_photo", userFile);
        formData.append("cloth_photo", clothBlob, "cloth.jpg");

        // Send to API endpoint
        const response = await fetch("https://api.yourservice.com/api/tryon", {
            method: "POST",
            body: formData
        });

        // Display the result
        const resultBlob = await response.blob();
        const imgUrl = URL.createObjectURL(resultBlob);
        const tryOnResultImg = document.createElement("img");
        tryOnResultImg.src = imgUrl;
        document.body.appendChild(tryOnResultImg);
    } catch (err) {
        console.error("Error while trying on clothes:", err);
    }
}
