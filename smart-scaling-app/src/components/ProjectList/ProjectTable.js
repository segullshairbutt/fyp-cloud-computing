import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import ProjectRow from './Project';

const ProjectTable = (props) => {
  return (
    <TableContainer component={Paper}>
      <Table aria-label="collapsible table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>User</TableCell>
            <TableCell>Version/Revisions</TableCell>
            <TableCell />
            <TableCell />
          </TableRow>
        </TableHead>
        <TableBody>
          {props.projects.map((project) => (
            <ProjectRow
              key={project.id}
              project={project}
              showProjectForm={props.showProjectForm}
              showDeleteProject={props.showDeleteProject}
            />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ProjectTable;
