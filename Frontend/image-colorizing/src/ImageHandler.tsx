import React, {useState} from 'react';
import './ImageHandler.css';
import loadingGif from './assets/loading.gif'
import download from './assets/download.png'
import {SnackbarProvider, useSnackbar} from 'notistack';

const ImageHandler: React.FC = () => {
    const {enqueueSnackbar} = useSnackbar();

    const [providedImageSrc, setProvidedImageSrc] = useState('');
    const [coloredImageSrc, setColoredImageSrc] = useState('');
    const [loading, setLoading] = useState<any>(false);

    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadMessage, setUploadMessage] = useState<string>('');

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file) {
            setSelectedFile(file);
            setUploadMessage('');

            setProvidedImageSrc('')
            setColoredImageSrc('')
        } else {
            setSelectedFile(null);
            setUploadMessage('Please select a valid image file.');
        }
    };

    const convertPath = (a: any) => a.replace('./uploads\\', 'http://localhost:5009/uploads/');

    function convertPathColorized(path: any) {
        return `http://localhost:5009/${path.replace(/\\/g, "/")}`;
    }

    function convertPathToUrlColorized(path: any) {
        return `http://localhost:5009/${path.replace(/\\/g, "/")}`;
    }

    const handleUpload = async () => {
        if (!selectedFile) {
            setUploadMessage('No file selected');
            return;
        }

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            setLoading(true);
            const response = await fetch('http://localhost:5009/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                setLoading(false);
                setUploadMessage(`Error uploading image: ${errorData.error}`);
            } else {
                setLoading(true);
                const data = await response.json();
                setProvidedImageSrc(convertPath(data.image_path));

                fetch("http://127.0.0.1:5009/colorize", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                })
                    .then(response => {
                        setLoading(false);
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        setLoading(false);
                        setColoredImageSrc(convertPathToUrlColorized(data.colorized_image_path));
                    })
                    .catch(error => {
                        enqueueSnackbar('Error:' + error, {variant: 'error'});
                        setLoading(false);
                        console.error('Error:', error);
                    });
                setUploadMessage(`Image uploaded successfully`);
            }
        } catch (error) {
            setLoading(false);
            console.error('Error uploading image:', error);
            enqueueSnackbar('Error:' + error, {variant: 'error'});
            setUploadMessage('Unexpected error occurred during upload.');
        }
    };

    const downloadColorized = () => {
        const link = document.createElement('a');
        link.href = coloredImageSrc;
        link.setAttribute('download', 'colorized_image.jpg');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    return (
        <div className="upload-container">
            <h1 className="title">Image Colorize</h1>
            <input type="file" className="file-input" accept="image/*" onChange={handleFileChange}/>
            <button className="upload-button" onClick={handleUpload}>Upload</button>
            {uploadMessage && <p className="upload-message">{uploadMessage}</p>}

            {(providedImageSrc && coloredImageSrc) && (
                <div>
                    <div>
                        <div className='image-title-container'>Provided Image:</div>
                        <img src={providedImageSrc} alt="Uploaded" style={{width: '300px', height: 'auto'}}/>
                    </div>
                    <div>
                        <div className='image-title-container'>Colored Image:</div>
                        <img src={coloredImageSrc} alt="Colored Image" style={{width: '300px', height: 'auto'}}/>
                        <div className='download-btn-container' onClick={downloadColorized}><img src={download} width='30px'/></div>
                    </div>
                </div>
            )}
            {loading &&
                <img src={loadingGif} width='50px' height='50px'/>
            }
        </div>
    );
};

export default ImageHandler;
