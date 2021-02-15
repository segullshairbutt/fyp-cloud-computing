import { Button, makeStyles, Typography } from '@material-ui/core';
import React from 'react';
import PropTypes from 'prop-types';

import Control from '../Control';

const Form = (props) => {
  const classes = useStyles();
  return (
    <form className={classes.Form}>
      <Typography variant="h5" align="center">
        {props.title}
      </Typography>
      {props.invalidForm && <p className={classes.ErrorText}>Please fill all required fields.</p>}
      {props.controls.map((control) => (
        <Control key={control.name} changed={props.changed} className={classes.Control} {...control} />
      ))}
      <br />
      <Button className={classes.Control} variant="contained" color="primary" onClick={props.submitted}>
        Submit
      </Button>
      <Button variant="contained" onClick={props.cancelled}>
        Cancel
      </Button>
    </form>
  );
};

Form.propTypes = {
  title: PropTypes.string.isRequired,
  changed: PropTypes.func.isRequired,
  controls: PropTypes.array.isRequired
};

export default Form;

const useStyles = makeStyles(() => ({
  Form: {
    margin: 'auto',
    width: '300px'
  },
  Control: {
    margin: '10px'
  },
  ErrorText: {
    color: 'red'
  }
}));
