// Update these constants to match whatever username and password you
// created your user with
const USERNAME = "tfedoris";
const PASSWORD = "mscs710!";

describe("Authenticator:", function () {
  // Step 1: before each test, we want to visit our app.
  // Note that this takes into account the base url that we
  // already configured. So the final address will be
  // "http://localhost:3000/"
  beforeEach(function () {
    cy.visit("/");
  });

  describe("Sign In:", () => {
    it("allows a user to signin", () => {
      // Step 2: Usually we can use cy.get to go locate the
      // button or field that we want to action directly, but
      // because of the shadow DOM, we can only use cy.get on
      // elements outside any shadow DOM. So here we get the element
      // outside the shadow DOM, and then use cy.find command, passing
      // in the "includeShadowDom: true" flag, to tell cypress to look
      // inside the shadow DOM.

      // Cypress commands are all asynchronise and can be chained together.
      // Which is what I'm doing here. If you want, you can read more about
      // it in the cypress documentation:
      // https://docs.cypress.io/guides/getting-started/writing-your-first-test.html#Add-a-test-file
      cy.get("amplify-authenticator")
        .find(selectors.usernameInput, {
          includeShadowDom: true,
        })
        .type(USERNAME);

      cy.get("amplify-authenticator")
        .find(selectors.signInPasswordInput, {
          includeShadowDom: true,
        })
        .type(PASSWORD, { force: true });

      // This one was a bit tricky to get to. It seems as though
      // there are two sign in buttons and cypress doesn't like
      // trying to click on two buttons at the same time,
      // so I'm chaining the .first() method to just take the
      // first button it finds.
      cy.get("amplify-authenticator")
        .find(selectors.signInSignInButton, {
          includeShadowDom: true,
        })
        .first()
        .find("button[type='submit']", { includeShadowDom: true })
        .click({ force: true });

      // Step 3: Make an assertion (Check for sign-out text)
      // By this stage we should be logged in. Cypress has many different
      // assertions. Here we're just checking to see if the page contains
      // the sign-out button.
      cy.get("amplify-sign-out")
        .find(selectors.signOutButton, { includeShadowDom: true })
        .contains("Sign Out");
    });
  });
});

export const selectors = {
  // Auth component classes
  usernameInput: 'input[data-test="sign-in-username-input"]',
  signInPasswordInput: 'input[data-test="sign-in-password-input"]',
  signInSignInButton: 'amplify-button[data-test="sign-in-sign-in-button"]',
  signOutButton: "amplify-button",
};
