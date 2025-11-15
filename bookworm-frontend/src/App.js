import React from 'react';

function BackgroundElements() {
  return (
    <div className="background-container">
      <div className="cloud cloud-1" style={{backgroundImage: 'url(/cloud1.png)'}}></div>
      <div className="cloud cloud-2" style={{backgroundImage: 'url(/cloud2.png)'}}></div>
      <div className="cloud cloud-3" style={{backgroundImage: 'url(/cloud3.png)'}}></div>
      <div className="cloud cloud-4" style={{backgroundImage: 'url(/cloud4.png)'}}></div>
      <div className="cloud cloud-5" style={{backgroundImage: 'url(/cloud5.png)'}}></div>
      <div className="cloud cloud-6" style={{backgroundImage: 'url(/cloud6.png)'}}></div>
      <div className="landscape-bg" style={{backgroundImage: 'url(/landscape.png)'}}></div>
    </div>
  );
}

function Header() {
  return (
    <header>
      <h1><a href="/">:: BookWorm ::</a></h1>
      <nav>
      </nav>
    </header>
  );
}

function LoginView() {
  return (
    <section id="login-view">
      <h2>LOGIN</h2>
      <form id="login-form" className="pixel-form">
        <div className="form-group">
          <label htmlFor="login-username">Username:</label>
          <input type="text" id="login-username" required />
        </div>
        <div className="form-group">
          <label htmlFor="login-password">Password:</label>
          <input type="password" id="login-password" required />
        </div>
        <button type="submit">Enter</button>
        <p>Nincs fiókod? <a href="/register">Regisztrálj</a></p>
      </form>
    </section>
  );
}


function App() {
  return (
    <>
      <BackgroundElements />
      
      <Header />
      <main>
        <LoginView />
      </main>
    </>
  );
}

export default App;