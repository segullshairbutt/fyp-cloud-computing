import Container from '@material-ui/core/Container';

import Appbar from './components/Appbar';
import ProjectList from './containers/ProjectList';
import ProjectForm from './components/ProjectForm';
import './App.css';

function App() {
  return [
    <Appbar />,
    <Container>
      <ProjectList />
      {/* <ProjectForm /> */}
    </Container>
  ];
}

export default App;
