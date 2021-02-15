import React from 'react';
import PropTypes from 'prop-types';
import { ErrorMessage, Field } from 'formik';

import Aux from '../../hoc/Auxx';

const Control = (props) => {
  let control = null;
  const style =
    props.errors && props.errors.length ? { ...styles.FormControl, ...styles.Error } : { ...styles.FormControl };

  switch (props.controltype) {
    case 'input':
      control = <Field style={style} name={props.name} {...props} />;
      break;
    case 'textarea':
      control = <Field style={style} as="textarea" name={props.name} {...props} />;
      break;
    case 'select':
      control = (
        <Field style={style} as="select" name={props.name} {...props}>
          {props.options &&
            props.options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
        </Field>
      );
      break;
    case 'checkbox':
      control = (
        <span>
          <label htmlFor={props.name}>{props.label} </label>
          <Field type="checkbox" name={props.name} checked={props.checked} />
          <br />
        </span>
      );
      break;
    case 'file':
      control = <input type="file" onChange={props.changed} name={props.name} {...props} />;
      break;
    default:
      control = null;
  }
  return (
    <Aux>
      {props.showLabel && <label>{props.label}</label>}
      {control}
      {/* to enable the error label give a errorLabeL Flag */}
      {props.errorLabel && <ErrorMessage style={{ color: 'red' }} name={props.name} component="div" />}
    </Aux>
  );
};

Control.propTypes = {
  controltype: PropTypes.string.isRequired,
  errors: PropTypes.array,
  errorLabel: PropTypes.bool,
  name: PropTypes.string.isRequired,
  changed: PropTypes.func.isRequired,
  label: PropTypes.string
};

export default Control;

const styles = {
  FormControl: {
    width: '100%',
    padding: '.5rem .4rem',
    fontSize: '1rem',
    borderRadius: '.3rem',
    outline: 'none',
    border: '1px solid black',
    boxShadow: '0 0 5px #3f51b5'
  },
  Error: {
    boxShadow: 'rgb(255,0,0) 0px 0px 5px'
  }
};
