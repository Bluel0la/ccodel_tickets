import { useState } from "react";

export default function Equation() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const apiBaseURL = "https://2uwwffk1kmr-496ff2e9c6d22116-8000-colab.googleusercontent.com"; // Replace with the actual FastAPI endpoint

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

 async function handleUpload(file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("https://your-colab-url/convert-latex", {
            method: "POST",
            body: formData,
            headers: {
                "Accept": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Response:", data);
    } catch (error) {
        console.error("Error:", error);
    }
}


  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-bold mb-4">Upload an Image</h2>
      
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="mb-4 w-full p-2 border rounded"
      />

      {preview && <img src={preview} alt="Preview" className="w-full h-48 object-contain mb-4" />}

      <div className="flex justify-between">
        <button
          onClick={() => handleUpload("convert-latex")}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
          disabled={loading}
        >
          Convert to LaTeX
        </button>

        <button
          onClick={() => handleUpload("convert-braille")}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-700"
          disabled={loading}
        >
          Convert to Braille
        </button>
      </div>

      {loading && <p className="mt-4 text-gray-600">Processing...</p>}

      {result && (
        <div className="mt-4 p-3 bg-gray-100 rounded text-sm">
          <strong>Result:</strong>
          <p className="text-gray-800">{result}</p>
        </div>
      )}
    </div>
  );
}
