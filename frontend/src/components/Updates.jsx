import React from 'react'

const Updates = ({ clsList }) => {
  return (
    <div className='flex flex-col items-center justify-start w-1/4 bg-gray-100 rounded-lg shadow-md m-4 p-2'>
      <table className="table-auto w-fit">
        <thead>
          <tr>
            <th className="border-green-600 border-2 px-4 py-2">Waste Classes</th>
            <th className="border-green-600 border-2 px-4 py-2">Encountered</th>
            <th className="border-green-600 border-2 px-4 py-2">Sorted</th>
          </tr>
        </thead>
        <tbody>
          {
            clsList.map((item, index) => {
              return (
                <tr key={item} className='bg-gray-100'>
                  <td className="border-green-600 border-2 px-4 py-2">{item}</td>
                  <td className="border-green-600 border-2 px-4 py-2">{index}</td>
                  <td className="border-green-600 border-2 px-4 py-2">{index + 1}</td>
                </tr>
              )
            })
          }
        </tbody>
      </table>
    </div>
  )
}

export default Updates