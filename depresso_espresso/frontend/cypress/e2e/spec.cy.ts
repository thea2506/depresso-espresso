describe('template spec', () => {
  it('login-logout', () => {
    cy.visit('https://depresso-espresso-7e0a859d2d18.herokuapp.com/site/signin')

    cy.get('#username').clear('te');
    cy.get('#username').type('test_account_cypress');
    cy.get('#password').clear();
    cy.get('#password').type('test123456');
    cy.get('.py-3').click();
    cy.get('.w-full > :nth-child(2) > svg').click();

    cy.get('.justify-first-line\\:center').click();
    cy.get('.z-50 > .w-full > :nth-child(3) > svg').click();
    cy.get('#root').click();
    cy.get(':nth-child(4) > svg').click();
    cy.get('.flex-col.items-center').click();
    cy.get('.flex > svg').click();

  })  



    it('test-2', () => {
      cy.visit('https://depresso-espresso-7e0a859d2d18.herokuapp.com/site/signin')

      cy.get('#username').clear('te');
      cy.get('#username').type('test_account_cypress');
      cy.get('#password').clear();
      cy.get('#password').type('test123456');
      cy.get('.py-3').click();

      cy.wait(2000)

      cy.get('.gap-y-12 > .flex > :nth-child(2)').click({ multiple: true });
      cy.get('[placeholder="Title"]').clear('te');
      cy.get('[placeholder="Title"]').type('test title');
      cy.get('[placeholder="Description"]').clear();
      cy.get('[placeholder="Description"]').type('test description');
      cy.get('#post-content').type('test content');
      cy.get(':nth-child(1) > .py-3').click();
      cy.get('.mt-2 > :nth-child(4)').click();
      cy.get('.h-full > .gap-y-4 > .flex-col > [placeholder="Title"]').clear('test title ');
      cy.get('.h-full > .gap-y-4 > .flex-col > [placeholder="Title"]').type('test title 2');
      cy.get('.h-full > .gap-y-4 > .flex-col > [placeholder="Description"]').clear('test description ');
      cy.get('.h-full > .gap-y-4 > .flex-col > [placeholder="Description"]').type('test description 2');
      cy.get('#post-content').click();
      cy.get('.h-full > .gap-y-4 > .flex-col > :nth-child(1) > .py-3').click();
      cy.get(':nth-child(1) > .p-3 > .mt-2 > :nth-child(5)').click();
      cy.get('.z-50 > .w-full > .flex > svg > path').click();

    })  

})