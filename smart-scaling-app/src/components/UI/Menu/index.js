import { Menu as MaterialMenu } from '@material-ui/core';
import PropTypes from 'prop-types';
import React from 'react';

const Menu = (props) => {
  return (
    <MaterialMenu
      id="menu-appbar"
      anchorEl={props.anchorEl}
      anchorOrigin={{
        vertical: 'top',
        horizontal: 'right'
      }}
      keepMounted
      transformOrigin={{
        vertical: 'top',
        horizontal: 'right'
      }}
      open={props.open}
      onClose={props.closed}
    >
      {props.children}
    </MaterialMenu>
  );
};

Menu.propTypes = {
  open: PropTypes.bool.isRequired,
  closed: PropTypes.func.isRequired,
  menuItems: PropTypes.array.isRequired
};

export default Menu;
