import React, { useState } from 'react'

const OptionsTable = ({ setClsList, setOptionsSelected }) => {
    const [selectedClasses, setSelectedClasses] = useState([]);
    const clsList = ["Can", "HDPE", "PET_Bottle", "Plastic_wrapper", "Tetrapak"]
    const handleChange = (value) => {
        // If checkbox is checked, add its value to the list
        // If checkbox is unchecked, remove its value from the list
        setSelectedClasses(prevState => {
            if (prevState.includes(value)) {
                return prevState.filter(item => item !== value);
            } else {
                return [...prevState, value];
            }
        });
    }

    const handleSumbit = () => {
        setOptionsSelected(true);
        setClsList(selectedClasses);
    }

    return (
        <div className='flex flex-col items-center justify-start w-1/4 bg-gray-100 rounded-lg shadow-md m-4 p-2'>
            <table className="table-auto w-fit">
                <thead>
                    <tr>
                        <th className="border-green-600 border-2 px-4 py-2">Sort</th>
                        <th className="border-green-600 border-2 px-4 py-2">Waste Classes</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        clsList.map(item => {
                            return (
                                <tr className='bg-gray-100'>
                                    <td className="border-green-600 border-2 px-4 py-2"><input type="checkbox" value={item} onChange={(e) => handleChange(e.target.value)} checked={selectedClasses.includes(item)} /></td>
                                    <td className="border-green-600 border-2 px-4 py-2">{item}</td>
                                </tr>
                            )
                        })
                    }
                </tbody>
            </table>
            <button
                onClick={handleSumbit}
                className="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue active:bg-blue-800"
            >
                Submit Options
            </button>
        </div>
    )
}

export default OptionsTable