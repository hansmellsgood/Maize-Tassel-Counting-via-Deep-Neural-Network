import React, { useRef, useState, useEffect, useReducer } from 'react';
import axios from 'axios';
import Scroll from 'react-scroll';
import Button from 'react-bootstrap/Button';

import './DropZone.css';

const returnContext = React.createContext({
    r: [], setR: () => {}

})

function Visualization() {
    const {r, setR} = React.useContext(returnContext)

    useEffect(() => {
    }, []);
    
    return (
        <>
        <div className='visualization multi-box row p-0 m-0'>
            {r.map((r) => (
                    <div className='col-md-6 col-lg-4'>
                        <div className='center'>
                            <img className='img-m mb-lg-10 ' src={r.display_img}/>
                        
                            <div className='single-results p-2'>
                                <div className='resultsDisplay'>
                                    <p className='text-center'>{r.file_name} <br />Count: {r.count}</p>
                                </div>
                            </div>
                        </div> 
                    </div>
            ))}
        </div></>
    )
}

const RadioGroup = () => {
    const [option, setOption] = React.useState('one');

  const handleOneChange = () => {
    setOption('one');
  };

  const handleTwoChange = () => {
    setOption('two');
  };

  const handleThreeChange = () => {
    setOption('three');
  };

  return (
    <div>
        <h5>Select Model</h5>
        <div>
            <RadioButton
                label=" Option 1"
                value={option === 'one'}
                onChange={handleOneChange}
            />
        </div>
        <div>
            <RadioButton
                label=" Option 2"
                value={option === 'two'}
                onChange={handleTwoChange}
            />
        </div>
        <div>
            <RadioButton
                label=" Option 3"
                value={option === 'three'}
                onChange={handleThreeChange}
            />
        </div>
    </div>
  );
};

const RadioButton = ({ label, value, onChange }) => {
    return (
      <label>
        <input type="radio" checked={value} onChange={onChange} />
        {label}
      </label>
    );
  };


const DropZoneM = () => {
    const fileInputRef = useRef();
    const modalImageRef = useRef();
    const modalRef = useRef();
    const progressRef = useRef();
    const uploadRef = useRef();
    const uploadModalRef = useRef();
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [validFiles, setValidFiles] = useState([]);
    const [unsupportedFiles, setUnsupportedFiles] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const [r, setR] = useState([]);
    const [display, setDisplay] = useState([]);
    const [rerender, setRerender] = useState(false);

    useEffect(() => {
        let filteredArr = selectedFiles.reduce((acc, current) => {
            const x = acc.find(item => item.name === current.name);
            if (!x) {
              return acc.concat([current]);
            } else {
              return acc;
            }
        }, []);
        setValidFiles([...filteredArr]);
    }, [selectedFiles]);

    const preventDefault = (e) => {
        e.preventDefault();
        // e.stopPropagation();
    }

    const dragOver = (e) => {
        preventDefault(e);
    }

    const dragEnter = (e) => {
        preventDefault(e);
    }

    const dragLeave = (e) => {
        preventDefault(e);
    }

    const fileDrop = (e) => {
        preventDefault(e);
        const files = e.dataTransfer.files;
        if (files.length) {
            handleFiles(files);
        }
    }

    const filesSelected = () => {
        if (fileInputRef.current.files.length) {
            handleFiles(fileInputRef.current.files);
        }
    }

    const fileInputClicked = () => {
        fileInputRef.current.click();
    }

    const handleFiles = (files) => {
        for(let i = 0; i < files.length; i++) {
            if (validateFile(files[i])) {
                setSelectedFiles(prevArray => [...prevArray, files[i]]);
            } else {
                files[i]['invalid'] = true;
                setSelectedFiles(prevArray => [...prevArray, files[i]]);
                setErrorMessage('File type not permitted');
                setUnsupportedFiles(prevArray => [...prevArray, files[i]]);
            }
        }
    }

    const validateFile = (file) => {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (validTypes.indexOf(file.type) === -1) {
            return false;
        }
        return true;
    }

    const fileSize = (size) => {
        if (size === 0) {
          return '0 Bytes';
        }
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(size) / Math.log(k));
        return parseFloat((size / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    const fileType = (fileName) => {
        return fileName.substring(fileName.lastIndexOf('.') + 1, fileName.length) || fileName;
    }

    const removeFile = (name) => {
        const index = validFiles.findIndex(e => e.name === name);
        const index2 = selectedFiles.findIndex(e => e.name === name);
        const index3 = unsupportedFiles.findIndex(e => e.name === name);
        validFiles.splice(index, 1);
        selectedFiles.splice(index2, 1);
        setValidFiles([...validFiles]);
        setSelectedFiles([...selectedFiles]);
        if (index3 !== -1) {
            unsupportedFiles.splice(index3, 1);
            setUnsupportedFiles([...unsupportedFiles]);
        }
    }

    const openImageModal = (file) => {
        const reader = new FileReader();
        modalRef.current.style.display = "block";
        reader.readAsDataURL(file);
        reader.onload = function(e) {
            modalImageRef.current.style.backgroundImage = `url(${e.target.result})`;
        }
    }

    const closeModal = () => {
        modalRef.current.style.display = "none";
        modalImageRef.current.style.backgroundImage = 'none';
    }

    const uploadFiles = async () => {
        uploadModalRef.current.style.display = 'block';
        uploadRef.current.innerHTML = 'File(s) Uploading...';
        const formData = new FormData();
        for (let i = 0; i < validFiles.length; i++) {
            formData.append('files', validFiles[i]);
            /*formData.append('key', '');*/
            /*https://api.imgbb.com/1/upload8 */
        }
        await axios.post('http://localhost:8000/testArray', formData, {       
            headers: {
                'Content-Type': "multipart/form-data"
            },
            onUploadProgress: (progressEvent) => {
                const uploadPercentage = Math.floor((progressEvent.loaded / progressEvent.total) * 100);
                progressRef.current.innerHTML = `${uploadPercentage}%`;
                progressRef.current.style.width = `${uploadPercentage}%`;

                if (uploadPercentage === 100) {
                    uploadRef.current.innerHTML = 'File(s) Uploaded';
                    validFiles.length = 0;
                    setValidFiles([...validFiles]);
                    setSelectedFiles([...validFiles]);
                    setUnsupportedFiles([...validFiles]);
                }
            },
        })
        .then ((rr) => {
            const rrr = rr.data;
            const r4 = rrr.data;
            for (let i = 0; i < r4.length; i++) {
                r4[i].image = 'data:image/jpeg;base64,' + r4[i].image
                r4[i].density_img = 'data:image/jpeg;base64,' + r4[i].density_img
                r4[i].display_img = r4[i].image
            }
            setR(r4)
        })
        .catch(() => {
            uploadRef.current.innerHTML = `<span class="error">Error Uploading File(s)</span>`;
            progressRef.current.style.backgroundColor = 'red';
        })            
    }

    const closeUploadModal = () => {
        uploadModalRef.current.style.display = 'none';
    }

    const ChangeIMG = () => {
        for (let i = 0; i < r.length; i++) {
            if (r[i].display_img === r[i].image) {
                r[i].display_img = r[i].density_img;
            }             
            else {
                r[i].display_img= r[i].image;
            }
        }
        setRerender(!rerender);
    };

    return (
        <>
        <returnContext.Provider value={{r, setR, display, setDisplay}}>
            <div className="container-fluid">
                <div className="vertical-align-top content top p-3">
                    <h2 className="font-weight-light">Multiple Upload</h2>
                    <hr/>
                    <div className="contain-box row">
                        <div className='col'>
                            <div className="drop-contain-box"
                                onDragOver={dragOver}
                                onDragEnter={dragEnter}
                                onDragLeave={dragLeave}
                                onDrop={fileDrop}
                                onClick={fileInputClicked}
                            >
                                <div className="drop-message">
                                    Drag & Drop files here or click to select file(s)
                                </div>
                                <input
                                    ref={fileInputRef}
                                    className="file-input"
                                    type="file"
                                    multiple
                                    onChange={filesSelected}
                                />
                            </div>
                            <div className='buttonmessage'>
                                {unsupportedFiles.length === 0 && validFiles.length ? <Button className="file-upload-btn center" variant="secondary" size="sm" onClick={() => uploadFiles()}>Upload</Button> : ''} 
                                {unsupportedFiles.length ? <p>Please remove all unsupported files.</p> : ''}
                            </div>
                        </div>
                        <div className='col'>
                            <Scroll.Element className="scroll-element" id="containerElement">
                            <div className="file-display-contain-box">
                                {
                                    validFiles.map((data, i) => 
                                        <div className="file-status-bar" key={i}>
                                            <div onClick={!data.invalid ? () => openImageModal(data) : () => removeFile(data.name)}>
                                                <div className="file-type-logo"></div>
                                                <div className="file-type">{fileType(data.name)}</div>
                                                <span className={`file-name ${data.invalid ? 'file-error' : ''}`}>{data.name}</span>
                                                <span className="file-size">({fileSize(data.size)})</span> {data.invalid && <span className='file-error-message'>({errorMessage})</span>}
                                            </div>
                                            <div className="file-remove" onClick={() => removeFile(data.name)}>X</div>
                                        </div>
                                    )
                                }
                            </div>
                            </Scroll.Element>
                        </div>  
                    </div>
                    <div className="modal" ref={modalRef}>
                        <div className="overlay"></div>
                        <span className="close" onClick={(() => closeModal())}>X</span>
                        <div className="modal-image" ref={modalImageRef}></div>
                    </div>
                    <div className="upload-modal" ref={uploadModalRef}>
                        <div className="overlay"></div>
                        <div className="close" onClick={(() => closeUploadModal())}>X</div>
                        <div className="progress-contain-box">
                            <span ref={uploadRef}></span>
                            <div className="progress">
                                <div className="progress-bar" ref={progressRef}></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="vertical-align-top content bottom p-3">
                    <h2 className="font-weight-light">Visualization</h2>
                    <hr/>
                    <div className='row'>
                    <div className='col-10'>
                        <Visualization />
                    </div>
                    <div className='col-2'>
                        <RadioGroup />
                        {/*
                        <div className='btn group'>
                            <Button variant="secondary" size="sm" className="visualization-btn" >Count Maize Tassels</Button>
                            <Button variant="secondary" size="sm" className="visualization-btn" >Density Map</Button>
                            <Button variant="secondary" size="sm" className="visualization-btn" >Download Image</Button>
                        </div>
                        */}
                        <div className='btn p-0 mt-3'>
                            <Button variant="secondary" size="sm" className="visualization-btn" onClick={ChangeIMG}>Toggle Visualisation</Button>
                        </div>
                    </div>
                    </div>
                    {/*}
                    <div className='btn group multiple-btn ml-3 mr-3 mb-3 p-0'>
                        <Button variant="secondary" size="sm" className="visualization-btnM" >Count Maize Tassels</Button>
                        <Button variant="secondary" size="sm" className="visualization-btnM" >Density Map</Button>
                        <Button variant="secondary" size="sm" className="visualization-btnM" >Download Image</Button>
                    </div>
                    */}
                    
                </div> 
            </div>
        </returnContext.Provider>
        </>
    );
}

export default DropZoneM;