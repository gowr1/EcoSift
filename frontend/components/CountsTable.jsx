import React from 'react'

const CountsTable = ({clsList}) => {
    return (
        <div className='flex items-center justify-center'>
            <table className="table-auto w-fit">
                <thead>
                    <tr>
                        <th className="px-4 py-2">CLass</th>
                        <th className="px-4 py-2">Counts</th>
                    </tr>
                </thead>
                <tbody>
                    <tr className='bg-gray-100'>
                        <td className="border px-4 py-2">Can</td>
                        <td className="border px-4 py-2">{clsList[0]}</td>
                    </tr>
                    <tr className='bg-gray-100'>
                        <td className="border px-4 py-2">HDPE</td>
                        <td className="border px-4 py-2">{clsList[1]}</td>
                    </tr>
                    <tr className='bg-gray-100'>
                        <td className="border px-4 py-2">PET_Bottle</td>
                        <td className="border px-4 py-2">{clsList[2]}</td>
                    </tr>
                    <tr className='bg-gray-100'>
                        <td className="border px-4 py-2">Tetrapak</td>
                        <td className="border px-4 py-2">{clsList[3]}</td>
                    </tr>
                    <tr className='bg-gray-100'>
                        <td className="border px-4 py-2">Plastic_wrapper</td>
                        <td className="border px-4 py-2">{clsList[4]}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}

export default CountsTable