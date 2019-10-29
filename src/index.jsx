import React from 'react';
import ReactDOM from 'react-dom';
import Block from './testComponent.jsx';
//<div>My Flask React App!</div>,

class App extends React.Component {
    render() {
        return (
            <Block />
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'));
