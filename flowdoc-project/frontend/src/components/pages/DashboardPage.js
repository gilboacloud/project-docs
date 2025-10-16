import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box
} from '@material-ui/core';
import Header from '../layout/Header';
import DocumentList from '../features/DocumentList';
import UploadDocument from '../features/UploadDocument';
import Statistics from '../features/Statistics';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'hidden'
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
    marginTop: 64
  },
  paper: {
    padding: theme.spacing(2),
    height: '100%'
  },
  title: {
    marginBottom: theme.spacing(2)
  }
}));

const DashboardPage = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Header />
      <main className={classes.content}>
        <Container maxWidth="lg">
          <Box mb={4}>
            <Typography variant="h4" className={classes.title}>
              Dashboard
            </Typography>
          </Box>
          
          <Grid container spacing={3}>
            {/* Statistics Overview */}
            <Grid item xs={12}>
              <Paper className={classes.paper}>
                <Statistics />
              </Paper>
            </Grid>

            {/* Document Upload */}
            <Grid item xs={12} md={4}>
              <Paper className={classes.paper}>
                <Typography variant="h6" gutterBottom>
                  Upload Document
                </Typography>
                <UploadDocument />
              </Paper>
            </Grid>

            {/* Recent Documents */}
            <Grid item xs={12} md={8}>
              <Paper className={classes.paper}>
                <Typography variant="h6" gutterBottom>
                  Recent Documents
                </Typography>
                <DocumentList />
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </main>
    </div>
  );
};

export default DashboardPage;