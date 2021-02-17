import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { Typography } from '@material-ui/core';

import TreeView from './TreeView';

export default function ProjectDetails(props) {
  const classes = useStyles();
  const { code } = props;
  const clusters = code.info['x-clusters'];
  const schemas = code.schemas;

  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={6}>
          <Paper className={classes.paper}>xs=6</Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={classes.paper}>
            <Grid item xs zeroMinWidth>
              <TreeView clusters={clusters} schemas={schemas} />
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary
  }
}));
