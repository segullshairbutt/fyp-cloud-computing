import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { Button } from '@material-ui/core';

import ConfirmationDialog from '../UI/ConfirmationDialog';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1
  }
}));

export default function MenuAppBar(props) {
  const classes = useStyles();
  const [ open, setOpen ] = useState(false);

  const disAgreed = () => {
    setOpen(false);
  };
  const agreed = () => {
    setOpen(false);
    props.deleted();
  };

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <ConfirmationDialog open={open} disagreed={disAgreed} agreed={agreed} />
          <Grid container spacing={1}>
            <Grid item xs={4}>
              <Typography variant="h6" className={classes.title}>
                {props.user}/{props.name}
              </Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography align="left" variant="h6">
                Status: {props.status}
              </Typography>
            </Grid>
            <Grid item xs={2}>
              {props.status !== 'Started' && (
                <Button variant="contained" color="primary" onClick={props.started} disabled={props.buttonsDisabled}>
                  Start Now
                </Button>
              )}
            </Grid>
            <Grid item xs={1}>
              <Button variant="contained" color="secondary" onClick={props.deleted} disabled={props.buttonsDisabled}>
                Delete
              </Button>
            </Grid>
          </Grid>
        </Toolbar>
      </AppBar>
    </div>
  );
}
