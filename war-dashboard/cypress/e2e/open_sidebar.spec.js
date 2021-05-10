// Update these constants to match whatever username and password you
// created your user with
const USERNAME = "tfedoris";
const PASSWORD = "mscs710!";

describe("Open Sidebar:", function () {
  // Step 1: before each test, we want to visit our app.
  // Note that this takes into account the base url that we
  // already configured. So the final address will be
  // "http://localhost:3000/"
  beforeEach(function () {
    cy.visit("/");
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
  });

  it("menu button opens the sidebar", () => {
    cy.get('[aria-label="open drawer"]').click();

    cy.get("#drawer").should("be.hidden");
  });
});

export const selectors = {
  // Auth component classes
  usernameInput: 'input[data-test="sign-in-username-input"]',
  signInPasswordInput: 'input[data-test="sign-in-password-input"]',
  signInSignInButton: 'amplify-button[data-test="sign-in-sign-in-button"]',
  signOutButton: "amplify-button",
};
