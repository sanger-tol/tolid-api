import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { example } from 'yargs';
import AddSpecies from './AddSpecies';

afterEach(() => {
    // remove the mock to ensure tests are completely isolated
    if (global.fetch.mock) {
        global.fetch.mockRestore();
    }
});

const inputSpeciesData = async (speciesData: string): Promise<HTMLInputElement> => {
    const input = screen.queryByRole('textbox');
    userEvent.type(input, speciesData);
    return input as HTMLInputElement;
}

const sendSpeciesData = async () => {
    const sendButton = screen.queryByRole('button');
    userEvent.click(sendButton);
}

it("no species data", async () => {
    // render component
    render(<AddSpecies />);
    
    // input empty data
    inputSpeciesData("").then(async input => {
        await sendSpeciesData();
        expect(input).toHaveProperty("validationMessage", "9 entries must be provided");
    })
});
