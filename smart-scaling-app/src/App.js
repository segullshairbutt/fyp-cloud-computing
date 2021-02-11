import Container from '@material-ui/core/Container';

import Appbar from './components/Appbar';
import Home from './containers/Home';
import './App.css';

function App() {
  return [
    <Appbar />,
    <Container>
      <Home />
    </Container>
  ];
}

export default App;
