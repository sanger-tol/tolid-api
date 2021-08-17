import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ErrorMessage } from '../../models/ErrorMessage';
import AddSpecies from './AddSpecies';

afterEach(() => {
    if (AddSpecies.prototype.mock) {
        AddSpecies.prototype.mockRestore()
    }
})

const inputSpeciesData = async (speciesData: string): Promise<HTMLInputElement> => {
    const input = screen.queryByRole('textbox');
    userEvent.type(input, speciesData);
    return input as HTMLInputElement;
}

const sendSpeciesData = async () => {
    const sendButton = screen.queryByRole('button');
    userEvent.click(sendButton);
}

const mockPostSpecies = (error: ErrorMessage) => {
    jest.spyOn(AddSpecies.prototype, "postSpecies").mockImplementation(
        async () => error
    );
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

it("incorrect number of species data fields", async () => {
    // render component
    render(<AddSpecies />);
    
    // input incorrect number of species data
    const badSpeciesData = "fake1\tfake2\tfake3";
    inputSpeciesData(badSpeciesData).then(async input => {
        await sendSpeciesData();
        expect(input).toHaveProperty("validationMessage", "9 entries must be provided");
    })
});

it("good species data", async () => {
    // render component
    render(<AddSpecies />);

    // input good species data
    const goodSpeciesData = "fake1\t\t\tfake2\tfake      3\t\tf a k e 4\tfake5\tfake6\t\t\tfake7\t\t\t fa ke 8\tfake9";
    inputSpeciesData(goodSpeciesData).then(async input => {
        await sendSpeciesData();
        expect(input).toHaveProperty("validationMessage", "");
    })
});

it("server-side error-message", async () => {
    // render component
    render(<AddSpecies />);

    // mock a server side error
    const errorDetail = "A very important error message";
    mockPostSpecies({
        title: "Server-Side Error",
        detail: errorDetail
    } as ErrorMessage);

    // send off request with good data
    const goodSpeciesData = "fake1\t\t\tfake2\tfake      3\t\tf a k e 4\tfake5\tfake6\t\t\tfake7\t\t\t fa ke 8\tfake9";
    inputSpeciesData(goodSpeciesData).then(async input => {
        await sendSpeciesData();
        // expect our server-side error to appear
        expect(input).toHaveProperty("validationMessage", errorDetail);
    })
});

