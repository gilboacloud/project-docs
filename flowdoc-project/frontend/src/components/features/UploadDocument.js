import React, { useState } from 'react';
import {
  Button,
  Typography,
  Box,
  LinearProgress,
  makeStyles
} from '@material-ui/core';
import { CloudUpload } from '@material-ui/icons';
import { DocumentService } from '../../services/documents';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  input: {
    display: 'none',
  },
  uploadButton: {
    marginTop: theme.spacing(2),
  },
  progress: {
    width: '100%',
    marginTop: theme.spacing(2),
  },
  successMessage: {
    color: theme.palette.success.main,
    marginTop: theme.spacing(2),
  },
  errorMessage: {
    color: theme.palette.error.main,
    marginTop: theme.spacing(2),
  },
}));

const UploadDocument = () => {
  const classes = useStyles();
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState({ success: false, message: '' });

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadStatus({ success: false, message: '' });
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    try {
      await DocumentService.uploadDocument(selectedFile, {
        fileName: selectedFile.name,
        fileType: selectedFile.type,
        uploadDate: new Date().toISOString(),
      });

      setUploadStatus({
        success: true,
        message: 'Document uploaded successfully!',
      });
      setSelectedFile(null);
    } catch (error) {
      setUploadStatus({
        success: false,
        message: 'Failed to upload document. Please try again.',
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className={classes.root}>
      <input
        accept="application/pdf,image/*"
        className={classes.input}
        id="upload-file"
        type="file"
        onChange={handleFileSelect}
      />
      <label htmlFor="upload-file">
        <Button
          variant="outlined"
          component="span"
          startIcon={<CloudUpload />}
          disabled={uploading}
        >
          Select File
        </Button>
      </label>

      {selectedFile && (
        <Box mt={2}>
          <Typography variant="body2">
            Selected: {selectedFile.name}
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={handleUpload}
            disabled={uploading}
            className={classes.uploadButton}
          >
            Upload
          </Button>
        </Box>
      )}

      {uploading && (
        <LinearProgress className={classes.progress} />
      )}

      {uploadStatus.message && (
        <Typography
          className={
            uploadStatus.success ? classes.successMessage : classes.errorMessage
          }
        >
          {uploadStatus.message}
        </Typography>
      )}
    </div>
  );
};

export default UploadDocument;