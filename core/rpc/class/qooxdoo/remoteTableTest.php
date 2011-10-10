<?php
  /*
   * qooxdoo - the new era of web development
   *
   * http://qooxdoo.org
   *
   * Copyright:
   *   2008 Derrell Lipman
   *
   * License:
   *   LGPL: http://www.gnu.org/licenses/lgpl.html
   *   EPL: http://www.eclipse.org/org/documents/epl-v10.php
   *   See the LICENSE file in the project's top-level directory for details.
   *
   * Authors:
   *  * Derrell Lipman (derrell)
   */

/*
 * This is a very simple example of server-generated data for a table which
 * uses a Remote Table Model.
 *
 * In this simple example, we provide each of the years between 1900 and 2020
 * inclusive, along with a boolean indicator of whether the year is/was a leap
 * year.  Table row 0 contains the data for year 1900, row 1 has year 1901,
 * etc.
 */

class class_remoteTableTest
{
    /**
     * Specify method accessibility.  Default value is configured in server,
     * but may be overridden on a per-method basis here.
     *
     * @param method
     *   The name of the method (without the leading "method_") to be tested
     *   for accessibility.
     *
     * @param defaultAccessibility
     *   The default accessibility configured in the server.  (See @return for
     *   possible values.)
     *
     * @param bScriptTransportInUse (not yet implemented)
     *   Boolean indicating whether the current request was issued via
     *   ScriptTransport.
     *
     * @param bDefaultScriptTransportAllowed (not yet implemented)
     *   Boolean specifying the default value for allowing requests via
     *   ScriptTransport. 
     *
     * @return
     *   One of these values:
     *     Accessibility_Public
     *     Accessibility_Domain
     *     Accessibility_Session
     *     Accessibility_Fail
     */
/*
    function GetAccessibility($method, $defaultAccessibility)
    {
        switch($method)
        {
        case "echo":
            return Accessibility_Domain;

        case "getInteger":
            return Accessibility_Session;

        case "getString":
            return Accessibility_Public;
        }

        return $defaultAccessibility;
    }
*/

    /**
     * Get the row count of the table
     *
     * @param params
     *   An array containing the parameters to this method.  None expected.
     *
     * @param error
     *   An object of class JsonRpcError.
     *
     * @return
     *   Success: The number of rows in the table
     *   Failure: null
     */
    function method_getRowCount($params, $error)
    {
        if (count($params) != 0)
        {
            $error->SetError(JsonRpcError_ParameterMismatch,
                             "Expected no parameters; got " . count($params));
            return $error;
        }

        // Since we're handling years 1900-2020 inclusive, we have a fixed
        // number of years, and thus a fixed row count.
        return 121;
    }

    /**
     * Get the row data, given a starting and ending row number.  In a "real"
     * backend for the Remote table model, one would likely retrieve row data
     * from a database or some other "massive" storage implementation.  In
     * this simple example, we dynamically generate the data.
     *
     * @param params
     *   An array containing the parameters to this method:
     *    params[0] : firstRow
     *    params[1] : lastRow
     *
     * @param error
     *   An object of class JsonRpcError.
     *
     * @return
     *   Success: The data model data for the requested rows.  The data is
     *            returned as an array of row arrays.  Each row array contains
     *            the year number as its first element and a boolean
     *            indicating whether that year is a leap year as its second
     *            element.
     *   Failure: null
     */
    function method_getRowData($params, $error)
    {
        if (count($params) != 2)
        {
            $error->SetError(JsonRpcError_ParameterMismatch,
                             "Expected 2 parameters; got " . count($params));
            return $error;
        }

        // Create an array of rows
        $rows = Array();

        // For each requested row...
        for ($row = $params[0],
                 $year = 1900 + $params[0];
             $row <= $params[1];
             $row++,
                 $year++)
        {
            // Create an array of data for this row
            $rowData = Array();

            // Get the data for this row.  In this example case, we calculate
            // it, but we could as well be retrieving it from a database.
            //
            // Note that the associative array indexes (which become the
            // property names in the JSON map) are the column id fields used
            // by the data model.  These are strings that are not localized
            // and so differ, possibly, from the column headings.
            $rowData["year"] = $year;
            $rowData["leap"] = (($year % 4 == 0 && $year % 100 != 0) ||
                                ($year %400 == 0));

            // Add this row data to the result set
            $rows[] = $rowData;
        }

        // Give 'em what they came for!
        return $rows;
    }
}

?>