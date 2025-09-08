//import { useState } from 'react'
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import "./App.css";

function App() {
  return (
    <>
      {/* Header */}
      <header>
        <h1>Biblioteca Virtual IFPB</h1>
        <nav>
          <a href="#buscar">Buscar</a>
          <a href="#">Início</a>
          <a href="#cursos">Cursos</a>
          <a href="#sobre">Sobre</a>
        </nav>
      </header>

      {/* Hero */}
      <section className="hero">
        <h2>Acesse materiais didáticos para apoiar seus estudos</h2>
        <p>
          Listas, livros e recursos digitais para os cursos técnicos integrados
          do IFPB - Campus Campina Grande.
        </p>
        <a href="#cursos" className="btn-primary">
          Explorar Cursos
        </a>
        <a href="#buscar" className="btn-secondary">
          Pesquisar Materiais
        </a>
      </section>

      {/* Cursos */}
      <section id="cursos" className="cursos">
        <h3>Cursos técnicos atendidos</h3>
        <div className="grid">
          <a href="#" className="card">
            <img
              src="/img/logoInformatica.png"
              alt="informatica"
              className="card-img"
            />
            <h4>Informática</h4>
          </a>
          <a href="#" className="card">
            <img
              src="/img/logoQuimica.png"
              alt="quimica"
              className="card-img"
            />
            <h4>Química</h4>
          </a>
          <a href="#" className="card">
            <img
              src="/img/logoPetroleoEGas.png"
              alt="petroleoGas"
              className="card-img"
            />
            <h4>Petróleo e Gás</h4>
          </a>
          <a href="#" className="card">
            <img
              src="/img/logoMineracao.png"
              alt="mineracao"
              className="card-img"
            />
            <h4>Mineração</h4>
          </a>
        </div>
      </section>

      {/* Buscar */}
      <section id="buscar" className="buscar">
        <h3>Buscar Materiais</h3>
        <input
          type="text"
          placeholder="  Busque por disciplina, autor ou palavra-chave"
        />
      </section>

      {/* Footer */}
      <footer>
        <p>Desenvolvido por alunos do IFPB - Campus Campina Grande</p>
      </footer>
    </>
  );
}

export default App;
