import logo from './logo.svg';
import './App.css';
import {HashRouter as Router, Route, Switch} from 'react-router-dom';
import Login from './components/Login';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/login" component={Login} />
      </Switch>
    </Router>
  );
}

export default App;
