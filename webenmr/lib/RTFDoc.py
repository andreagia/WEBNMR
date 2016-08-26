import os, sys
from PyRTF import *


def buildDOC(info):
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    #p = Paragraph( ss.ParagraphStyles.Heading1 )
    #p.append( 'Summary of %s and structural statistics for %s project' %(info['typestr'], info['projname']) )
    #section.append( p )

    # changes what is now the default style of Heading1 back to Normal
    #p = Paragraph( ss.ParagraphStyles.Normal )
    #p.append( 'Example 3 demonstrates tables, tables represent one of the '
    #          'harder things to control in RTF as they offer alot of '
    #          'flexibility in formatting and layout.' )
    #section.append( p )
    #
    #section.append( 'Table columns are specified in widths, the following example '
    #                'consists of a table with 3 columns, the first column is '
    #                '7 tab widths wide, the next two are 3 tab widths wide. '
    #                'The widths chosen are arbitrary, they do not have to be '
    #                'multiples of tab widths.' )

    table = Table( TabPS.DEFAULT_WIDTH * 9,
                   TabPS.DEFAULT_WIDTH * 3)
    
    ch = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'Sedimented solute NMR parameters'   ) )
    chempty = Cell( Paragraph( '' ) )
    table.AddRow(ch, chempty)
    c1prop = Cell( Paragraph( ss.ParagraphStyles.Normal, 'Threshold (%)'   ) )
    c1val = Cell( Paragraph( ss.ParagraphStyles.Normal, info['threshold']   ) )
    table.AddRow(c1prop, c1val)
    c2prop = Cell( Paragraph( 'Temperature (K)' ) )
    c2val = Cell( Paragraph( info['temperature'] ) )
    table.AddRow(c2prop, c2val)
    c3prop = Cell( Paragraph( 'Protein molecular weight (kDa)' ) )
    c3val = Cell( Paragraph( info['protmw']) )
    table.AddRow(c3prop, c3val)
    c4prop = Cell( Paragraph( 'Initial concentration (mg/ml)' ) )
    c4val = Cell( Paragraph( info['initconc']) )
    table.AddRow(c4prop, c4val)
    c5prop = Cell( Paragraph( 'Limit concentration (mg/ml)' ) )
    c5val = Cell( Paragraph( info['limitconc']) )
    table.AddRow(c5prop, c5val)
    c6prop = Cell( Paragraph( 'Protein density (g/ml)' ) )
    c6val = Cell( Paragraph( info['protdens']) )
    table.AddRow(c6prop, c6val)
    c7prop = Cell( Paragraph( 'solvent density (g/ml)' ) )
    c7val = Cell( Paragraph( info['solvdens']) )
    table.AddRow(c6prop, c7val)
    if info["devrot"] == 'rotor':
        c8prop = Cell( Paragraph( 'MAS frequency (Hz)' ) )
        c8val = Cell( Paragraph( info['masfreq']) )
        table.AddRow(c8prop, c8val)
        c9prop = Cell( Paragraph( 'Rotor radius (mm)' ) )
        c9val = Cell( Paragraph( info['rotradius']) )
        table.AddRow(c9prop, c9val)
    else:
        c8aprop = Cell( Paragraph( 'Centrifugation speed (rpm)' ) )
        c8aval = Cell( Paragraph( info['censpeed']) )
        table.AddRow(c8aprop, c8aval)
        c8prop = Cell( Paragraph( 'hfun (cm)' ) )
        c8val = Cell( Paragraph( info['hfun']) )
        table.AddRow(c8prop, c8val)
        c9prop = Cell( Paragraph( 'hmax (cm)' ) )
        c9val = Cell( Paragraph( info['hmax']) )
        table.AddRow(c9prop, c9val)
        c10prop = Cell( Paragraph( 'htot (cm)' ) )
        c10val = Cell( Paragraph( info['htot']) )
        table.AddRow(c10prop, c10val)
        c11prop = Cell( Paragraph( 'h1 (cm)' ) )
        c11val = Cell( Paragraph( info['h1']) )
        table.AddRow(c11prop, c11val)
        c12prop = Cell( Paragraph( 'h2 (cm)' ) )
        c12val = Cell( Paragraph( info['h2']) )
        table.AddRow(c12prop, c12val)
        c13prop = Cell( Paragraph( 'h3 (cm)' ) )
        c13val = Cell( Paragraph( info['h3']) )
        table.AddRow(c13prop, c13val)
        c14prop = Cell( Paragraph( 'r1 (cm)' ) )
        c14val = Cell( Paragraph( info['r1']) )
        table.AddRow(c14prop, c14val)
        c15prop = Cell( Paragraph( 'r2 (cm)' ) )
        c15val = Cell( Paragraph( info['r2']) )
        table.AddRow(c15prop, c15val)
        c16prop = Cell( Paragraph( 'r3 (cm)' ) )
        c16val = Cell( Paragraph( info['r3']) )
        table.AddRow(c16prop, c16val)
    section.append( table )
    
    return doc
    
#def openFile( name ) :
#    return file( '%s' % name, 'w' )

def saveToFile(doc, filename, where):
    DR = Renderer()
    DR.Write( doc, file( os.path.join(where, filename), 'w' ))
    
#if __name__ == '__main__' :
#    DR = Renderer()
#    info = {'typestr': 'NMR', 'projname': 'TestRTF'}
#    rtfBuilder = RTFDoc()
#    doc = RTFDoc.buildDOC(info)
#    DR.Write( doc, openFile( info['projname'] ) )
#    
#    print "Finished"

