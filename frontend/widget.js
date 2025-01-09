async function tryOnClothes(userFile, clothFile, storeId) {
  try {
    console.log("Starting try-on process...");
    console.log("Files received:", {
      userFile: userFile?.name,
      clothFile: clothFile?.name,
      storeId,
    });

    // Create FormData
    const formData = new FormData();
    formData.append("store_id", storeId);
    formData.append("user_photo", userFile);
    formData.append("cloth_photo", clothFile);

    console.log("Sending request to server...");

    // Send to API endpoint
    const response = await fetch("http://localhost:8000/api/tryon", {
      method: "POST",
      body: formData,
    });

    console.log("Server response status:", response.status);

    // Log the response headers
    console.log("Response headers:", Object.fromEntries([...response.headers]));

    if (!response.ok) {
      // Try to get error details from response
      let errorDetail;
      try {
        const errorJson = await response.json();
        errorDetail = JSON.stringify(errorJson);
      } catch (e) {
        errorDetail = await response.text();
      }

      throw new Error(
        `HTTP error! status: ${response.status}, details: ${errorDetail}`
      );
    }

    // Check the content type of the response
    const contentType = response.headers.get("content-type");
    console.log("Response content type:", contentType);

    // Display the result
    const resultBlob = await response.blob();
    console.log("Received blob:", {
      size: resultBlob.size,
      type: resultBlob.type,
    });

    const imgUrl = URL.createObjectURL(resultBlob);

    // Clear previous results
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    // Add new result image
    const tryOnResultImg = document.createElement("img");
    tryOnResultImg.src = imgUrl;
    tryOnResultImg.className = "result-image";
    tryOnResultImg.onerror = (e) => {
      console.error("Error loading result image:", e);
      resultDiv.innerHTML =
        '<p style="color: red;">Error displaying result image</p>';
    };
    resultDiv.appendChild(tryOnResultImg);
  } catch (err) {
    console.error("Error while trying on clothes:", err);
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `<p style="color: red;">Error: ${err.message}</p>`;
  }
}

