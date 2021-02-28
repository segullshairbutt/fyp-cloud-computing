import Container from '@material-ui/core/Container';
import { Route } from 'react-router-dom';

import ProjectList from './containers/ProjectList';
import Swagger from './containers/SwaggerUI';
import ProjectDetail from './containers/ProjectDetail';
import './App.css';

function App() {
  return [
    <Container>
      <Route path="/:id/swagger/:filename" component={Swagger} />
      <Route exact path="/:id" component={ProjectDetail} />
      <Route exact path="/" component={ProjectList} />

      {/* <ProjectDetail /> */}
    </Container>
  ];
}

export default App;
