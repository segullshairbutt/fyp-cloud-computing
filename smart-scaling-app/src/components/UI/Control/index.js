import React from 'react';
import PropTypes from 'prop-types';

import Aux from '../../hoc/Auxx';

const Control = (props) => {
  let control = null;
  const style =
    props.errors && props.errors.length ? { ...styles.FormControl, ...styles.Error } : { ...styles.FormControl };

  switch (props.controltype) {
    case 'input':
      control = (
        <input
          style={style}
          ref={props.ref}
          control={props.control}
          name={props.name}
          value={props.value}
          onChange={props.changed}
          {...props}
        />
      );
      break;
    case 'select':
      control = (
        <select style={style} name={props.name} value={props.value} onChange={props.changed} {...props}>
          {props.options && props.options.map((option) => <option value={option.value}>{option.label}</option>)}
        </select>
      );
      break;
    case 'checkbox':
      control = (
        <span>
          <label htmlFor="vehicle1">{props.label} </label>
          <input type="checkbox" name={props.name} checked={props.checked} onChange={props.changed} />
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
      {control}
      {/* to enable the error label give a errorLabeL Flag */}
      {props.errorLabel &&
        props.errors &&
        props.errors.map((error, index) => (
          <Aux>
            <small style={{ color: 'red' }} key={index}>
              {error}
            </small>
            <br />
          </Aux>
        ))}
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
