import React from 'react';
import PropTypes from 'prop-types';

import ConfirmatioDialog from '../Dialog';

export default function ConfirmationDialog(props) {
  return (
    <ConfirmatioDialog
      size="sm"
      open={props.open}
      successText={'Agree'}
      successful={props.agreed}
      cancelText={'Disagree'}
      cancelled={props.disagreed}
    >
      This is irreverable. Do you really want to proceed?
    </ConfirmatioDialog>
  );
}

ConfirmationDialog.propTypes = {
  disagreed: PropTypes.bool,
  agreed: PropTypes.bool
};
