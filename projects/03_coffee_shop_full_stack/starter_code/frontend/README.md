# Coffee Shop Frontend

## Getting Setup

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).
> Note: https://stackoverflow.com/questions/16904658/node-version-manager-install-nvm-command-not-found

#### Installing Ionic Cli and project dependencies

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository.

> Note: https://knowledge.udacity.com/questions/382716

```
to proper install ionic:

[...]
4. nvm ls-remote
5. nvm install 12.10.0
6. npm install -g cordova
7. npm install -g ionic
8. npm install -g @angular/cli
9. npm install --save-dev @angular-devkit/build-angular
10. ionic -v

common issues:

The ng was not found, just run:

npm install -g angular-cli

If node-sass not found:

npm install --save-dev node-sass

The specified command run is invalid. For available options, see `ng help`. [ERROR] ng has unexpectedly closed (exit code 1).

npm install @ionic/app-scripts@latest --save-dev
ionic repair
```

## Required Tasks

### Configure Enviornment Variables

Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

- Open `./src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.

## Running Your Frontend in Dev Mode

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```

>_tip_: Do not use **ionic serve**  in production. Instead, build Ionic into a build artifact for your desired platforms.
[Checkout the Ionic docs to learn more](https://ionicframework.com/docs/cli/commands/build)

## Key Software Design Relevant to Our Coursework

The frontend framework is a bit beefy; here are the two areas to focus your study.

### Authentication

The authentication system used for this project is Auth0. `./src/services/auth.service.ts` contains the logic to direct a user to the Auth0 login page, managing the JWT token upon successful callback, and handle setting and retrieving the token from the local store. This token is then consumed by our DrinkService (`./src/services/auth.service.ts`) and passed as an Authorization header when making requests to our backend.

### Authorization

The Auth0 JWT includes claims for permissions based on the user's role within the Auth0 system. This project makes use of these claims using the `auth.can(permission)` method which checks if particular permissions exist within the JWT permissions claim of the currently logged in user. This method is defined in  `./src/services/auth.service.ts` and is then used to enable and disable buttons in `./src/pages/drink-menu/drink-form/drink-form.html`.