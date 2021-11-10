/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ErrorMessage } from '../../models/ErrorMessage';
import AddSpecies from './AddSpecies';
import { AxiosResponse, AxiosError, AxiosRequestConfig } from 'axios';
import { act } from 'react-dom/test-utils';

const inputSpeciesData = async (speciesData: string): Promise<HTMLInputElement> => {
    const input = screen.queryByRole('textbox') as HTMLInputElement;
    await act(async () => {
        userEvent.type(input, speciesData);
    });
    return input as HTMLInputElement;
}

const sendSpeciesData = async () => {
    const sendButton = screen.queryByRole('button') as HTMLElement;
    await act(async () => {
        userEvent.click(sendButton);
    });
}

const mockPostSpecies = (error: ErrorMessage) => {
    const httpClientModule = require('../../services/http/httpClient');
    httpClientModule.httpClient = jest.fn(() => ({
        get: jest.fn(),
        post: jest.fn(async () => {
            throw {
                config: {} as AxiosRequestConfig,
                toJSON: () => {},
                isAxiosError: true,
                response: {
                    data: error,
                    status: 400,
                    statusText: ""
                } as AxiosResponse<ErrorMessage>
            } as AxiosError<ErrorMessage>;
        }),
        put: jest.fn(),
        patch: jest.fn(),
        delete: jest.fn()
    }));
}

it("no species data", async () => {
    // render component
    render(<AddSpecies/>);
    
    // input empty data
    inputSpeciesData("").then(async input => {
        await sendSpeciesData();
        expect(input).toHaveProperty("validationMessage", "9 entries must be provided");
    })
});

it("incorrect number of species data fields", async () => {
    // render component
    render(<AddSpecies/>);
    
    // input incorrect number of species data
    const badSpeciesData = "fake1\tfake2\tfake3";
    inputSpeciesData(badSpeciesData).then(async input => {
        await sendSpeciesData();
        expect(input).toHaveProperty("validationMessage", "9 entries must be provided");
    })
});

it("Non integer taxonomy id", async () => {
    // render component
    render(<AddSpecies/>);
    
    // input otherwise correct data, except the taxonomy id (3rd) should be an integer
    const badSpeciesData = "fake1\t\t\tfake2\tfake      3\t\tf a k e 4\tfake5\tfake6\t\t\tfake7\t\t\t fa ke 8\tfake9";
    inputSpeciesData(badSpeciesData).then(async input => {
        await sendSpeciesData();
        expect(input).toHaveProperty("validationMessage", "The taxonomy ID (3rd entry) must be an integer");
    })
});

it("good species data", async () => {
    // render component
    render(<AddSpecies/>);

    // input good species data
    const goodSpeciesData = "fake1\t\t\tfake2\t1234567890\t\t\n\nf a k e 4\tfake5\tfake6\t\t\tfake7\t\t\t fa ke 8\nfake9";
    inputSpeciesData(goodSpeciesData).then(async input => {
        await sendSpeciesData();
        expect(input).toHaveProperty("validationMessage", "");
        expect(screen.getByText("Species added successfully!")).toBeInTheDocument();
    });
});

it("server-side error-message", async () => {
    // render component
    act(() => {
        render(<AddSpecies/>);
    });

    // mock a server side error
    const errorDetail = "A very important error message";
    mockPostSpecies({
        title: "Server-Side Error",
        detail: errorDetail
    } as ErrorMessage);

    // send off request with good data
    const goodSpeciesData = "fake1\t\t\tfake2\t1234567890\t\t\n\nf a k e 4\tfake5\tfake6\t\t\tfake7\t\t\t fa ke 8\nfake9";
    inputSpeciesData(goodSpeciesData).then(async input => {
        await sendSpeciesData();
        // expect our server-side error to appear, have to wait half a second
        setTimeout(() => {
            act(async () => {
                expect(input).toHaveProperty("validationMessage", errorDetail);
                expect(screen.getByText("Species added successfully!")).not.toBeInTheDocument();
            });
        }, 500
        )
    });
});
