import React from 'react';
import { Button, IconButton } from '@material-ui/core';
import styled from 'styled-components';
import CancelIcon from '@material-ui/icons/Cancel';
import AddIcon from '@material-ui/icons/Add';

import Aux from '../hoc/Auxx';

const NodeFields = (props) => {
  return (
    <Aux>
      {props.fields.map(({ cpu, ram }, index) => {
        return (
          <FieldArrayFormDiv key={index}>
            <CustomInput
              type="number"
              defaultValue={cpu}
              placeholder="CPU"
              name={`nodes[${index}].cpu`}
              register={props.register({
                required: true
              })}
            />
            <CustomInput
              type="number"
              defaultValue={cpu}
              placeholder="RAM"
              name={`nodes[${index}].ram`}
              register={props.register({
                required: true
              })}
            />
            <IconButton
              style={{ marginTop: '-.4rem' }}
              color="secondary"
              variant="contained"
              onClick={() => props.remove(index)}
            >
              <CancelIcon />
            </IconButton>
          </FieldArrayFormDiv>
        );
      })}
      {props.isSaving && (
        <p style={{ color: 'yellowgreen' }}>Never forget to click on Save Changes above to save everything !!</p>
      )}
      <FieldArrayFormDiv>
        <Button
          color="primary"
          onClick={() =>
            props.append({
              cpu: '',
              ram: ''
            })}
        >
          <AddIcon /> Add Node
        </Button>
        <Button type="submit" color="primary" variant="contained" disabled={props.isSaving}>
          Save
        </Button>
      </FieldArrayFormDiv>
    </Aux>
  );
};

export default NodeFields;

const FieldArrayFormDiv = styled.div`
  margin: 0.3rem 0;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
`;

export const inputStyle = {
  width: '100%',
  padding: '.5rem .4rem',
  fontSize: '1rem',
  borderRadius: '.3rem',
  outline: 'none',
  border: '1px solid black',
  boxShadow: '0 0 5px #3f51b5'
};
const CustomInput = (props) => (
  <div>
    <input
      style={inputStyle}
      type={props.type}
      name={props.name}
      placeholder={props.placeHolder}
      ref={props.register}
      onKeyDown={props.OnKeyDown}
      control={props.control}
      onChange={props.onChangeHandler}
      disabled={props.disabled}
      {...props}
    />
  </div>
);
