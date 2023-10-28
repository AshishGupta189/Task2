document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById("file");
    const submitButton = document.getElementById("submit");
    const summaryText = document.getElementById("summary-text");

    submitButton.addEventListener("click", async () => {
        const files = document.querySelector('input[type="file"]').files;
        const formData = new FormData();
        const url='http://127.0.0.1:5000/summarize'
        if(files.length==0){
            alert("Please select a file to upload.");
        }else{
            for (const file of files) {
                formData.append('file', file);
            }
            const response = await fetch(url, {
                method: "POST",
                body: formData,
            });
            if (response.status === 200) {
                const data = await response.json();
                summaryText.textContent = data.summary;
            } else {
                summaryText.textContent = "Error: Unable to generate a summary.";
            }
        }
        
    });
});
