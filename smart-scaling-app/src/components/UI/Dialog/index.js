import React from 'react';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { useTheme } from '@material-ui/core/styles';
import PropTypes from 'prop-types';

export default function ConfirmationDialog(props) {
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down(props.size));

  return (
    <div>
      <Dialog
        fullScreen={fullScreen}
        open={props.open}
        onClose={props.disagree}
        aria-labelledby="responsive-dialog-title"
      >
        <DialogTitle id="responsive-dialog-title" align="center">
          {props.title}
        </DialogTitle>
        <DialogContent>
          <DialogContentText>{props.children}</DialogContentText>
        </DialogContent>
        {!props.hideActions && (
          <DialogActions>
            <Button autoFocus onClick={props.cancelled} color="primary">
              {props.cancelText}
            </Button>
            <Button onClick={props.successful} color="primary" autoFocus>
              {props.successText}
            </Button>
          </DialogActions>
        )}
      </Dialog>
    </div>
  );
}

ConfirmationDialog.propTypes = {
  hideActions: PropTypes.bool,
  open: PropTypes.bool,
  successful: PropTypes.func,
  cancelled: PropTypes.func,
  cancelText: PropTypes.string,
  successText: PropTypes.string,
  children: PropTypes.any,
  title: PropTypes.string.isRequired
};
