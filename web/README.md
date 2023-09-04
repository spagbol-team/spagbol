# How to run

## Without Docker

this repo use Yarn. Feel free to use NPM.

```
yarn && yarn dev
```

## With Docker

make sure your Docker is running. e.g. Docker Desktop is running for MacOS or Windows.

first time running this?

```
yarn docker-initiate
```

otherwise:

```
yarn docker-dev
```

## ISSUES

```
failed to load config from /<loc>/vite.config.js
```

if you're using MacOS or windows you might not want to switch between using docker and non docker (using yarn dev and yarn docker-dev interchangeably) as docker will install dependencies in linux-x64. Use just one of it.
otherwise you'll need to reinstall the node_modules

# Tech Stack

- React + Vite
- Tailwind
- Plotly.js

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh
