import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import DetailsIcon from '@material-ui/icons/Details';
import DeleteIcon from '@material-ui/icons/Delete';
import { Link } from 'react-router-dom';

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
        <TableCell>{project.config ? project.config.tag : 'None'}</TableCell>
        <TableCell>{project.config ? 'Running' : 'Pending'}</TableCell>
        <TableCell>
          <Link to={'/' + props.id}>
            <IconButton aria-label="expand row" size="small">
              <DetailsIcon />
            </IconButton>
          </Link>
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
