describe('template spec', () => {
  it('passes', () => {
    cy.visit('https://depresso-espresso-7e0a859d2d18.herokuapp.com/site/signin')

    cy.get('#username').clear('te');
    cy.get('#username').type('test_account_cypress');
    cy.get('#password').clear();
    cy.get('#password').type('test123456');
    cy.get('.py-3').click();
    cy.get('.w-full > :nth-child(2) > svg').click();


    /* ==== Generated with Cypress Studio ==== */
    cy.get('.justify-first-line\\:center').click();
    cy.get('.z-50 > .w-full > :nth-child(3) > svg').click();
    cy.get('#root').click();
    cy.get(':nth-child(4) > svg').click();
    cy.get('.flex-col.items-center').click();
    cy.get('.flex > svg').click();
    /* ==== End Cypress Studio ==== */
  })
})