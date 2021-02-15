import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import EditIcon from '@material-ui/icons/Edit';
import DeleteIcon from '@material-ui/icons/Delete';

const useRowStyles = makeStyles({
  root: {
    '& > *': {
      borderBottom: 'unset'
    }
  },
  addButtonStyle: {
    marginLeft: '10px'
  }
});

const Project = (props) => {
  const { project } = props;
  const classes = useRowStyles();

  return (
    <React.Fragment>
      <TableRow className={classes.root}>
        <TableCell component="th" scope="row">
          {project.name}
        </TableCell>
        <TableCell>{project.username}</TableCell>
        <TableCell>{project.config.tag}</TableCell>
        <TableCell>Running</TableCell>
        <TableCell>
          <IconButton aria-label="expand row" size="small" onClick={props.showProjectForm}>
            <EditIcon />
          </IconButton>
        </TableCell>
        <TableCell>
          <IconButton aria-label="expand row" size="small" onClick={props.showDeleteProject}>
            <DeleteIcon />
          </IconButton>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
};

export default Project;
