import React, { useState } from 'react';
import TextField from '@material-ui/core/TextField';
import { Typography, Paper, Link, Grid, Button, CssBaseline } from '@material-ui/core';

const onSubmit = async (values) => {
  debugger;
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  await sleep(300);
  window.alert(JSON.stringify(values, 0, 2));
};

const Home = (props) => {
  const [ values, setValues ] = useState({ name: '', notes: '' });
  const onChange = (e) => {
    const oldValues = { ...values };
    oldValues[e.target.name] = e.target.value;
    setValues({ ...oldValues });
  };

  return (
    <div style={{ padding: 16, margin: 'auto', maxWidth: 600 }}>
      <CssBaseline />
      <Typography variant="h4" align="center" component="h1" gutterBottom>
        Smart Horizontal and Vertical Scaling Application
      </Typography>
      <Typography variant="h5" align="center" component="h2" gutterBottom>
        Open-Api-Based Configurations
      </Typography>
      <Typography paragraph>
        <Link href="https://github.com/erikras/react-final-form#-react-final-form">Read Docs</Link>
        . This example demonstrates using <Link href="https://material-ui.com/demos/text-fields/">
          Material-UI
        </Link>{' '}
        form controls.
      </Typography>
      <form onSubmit={props.formSubmitted} noValidate>
        <Paper style={{ padding: 16 }}>
          <Grid container alignItems="flex-start" spacing={2}>
            <Grid item xs={12}>
              <TextField
                name="name"
                fullWidth
                type="text"
                label="Project Name"
                value={values.name}
                onChange={onChange}
              />
              <small>name of project is required.</small>
            </Grid>
            <Grid item xs={12}>
              <input
                accept="application/JSON"
                hidden
                id="raised-button-file"
                type="file"
                required
                onChange={props.fileUploaded}
              />
              <label htmlFor="raised-button-file">
                <Button variant="raised" component="span">
                  {props.fileName}
                </Button>
              </label>
              {props.fileError && <small>config file is required.</small>}
            </Grid>
            <Grid item xs={12}>
              <TextField fullWidth name="notes" multiline label="Notes" value={values.notes} onChange={onChange} />
            </Grid>
            <Grid item style={{ marginTop: 16 }}>
              <Button type="button" variant="contained">
                Reset
              </Button>
            </Grid>
            <Grid item style={{ marginTop: 16 }}>
              <Button variant="contained" color="primary" type="submit">
                Submit
              </Button>
            </Grid>
          </Grid>
        </Paper>
        {/* <pre>{JSON.stringify(props.text, 0, 2)}</pre> */}
        <pre>{props.text}</pre>
      </form>
    </div>
  );
};

export default Home;
