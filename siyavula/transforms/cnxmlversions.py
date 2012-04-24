from lxml import etree

conversionChain = ['0.0', '0.1']


def v0_0_to_v0_1(iDom):
    """
    Convert exercise environments. Old format: all problems are listed
    first, followed by shortcodes with urls/solutions. New format:
    exercise environment contains any number of entries; each entry
    contains one problem, one shortcode and one solution/url.

    Modifies the DOM *in place*.
    """
    versionNode = iDom.xpath('/document/metadata/cnxml-version')[0]
    assert versionNode.text == '0.0'
    versionNode.text = '0.1'
    for oldExerciseNode in iDom.xpath('//exercise'):
        newExercisesNode = etree.Element('exercises')
        titleNode = oldExerciseNode.find('title')
        if titleNode is None:
            titleNode = etree.Element('title')
        newExercisesNode.append(titleNode)

        oldShortcodesNode = oldExerciseNode.find('shortcodes')
        oldShortcodesIndex = 0

        problemNumber = 1
        for problemNode in oldExerciseNode.xpath('./problem'):
            entryNode = etree.Element('entry')
            entryNode.text = '\n'
            entryNode.tail = '\n'
            newExercisesNode.append(entryNode)
            assert oldShortcodesNode[oldShortcodesIndex].find('number').text == str(problemNumber), "Non-consecutive integer numbering (expected %i, got %s)"%(problemNumber, oldShortcodesNode[oldShortcodesIndex].find('number').text)
            entryNode.append(oldShortcodesNode[oldShortcodesIndex].find('shortcode'))
            entryNode[-1].tail = '\n'
            entryNode.append(problemNode)
            solutionNode = oldShortcodesNode[oldShortcodesIndex].find('content')
            urlNode = oldShortcodesNode[oldShortcodesIndex].find('url')
            if solutionNode is not None:
                solutionNode.tag = 'solution'
                if urlNode is not None:
                    solutionNode.attrib['url'] = urlNode.text
            else:
                assert urlNode is not None
                solutionNode = etree.Element('solution', url=urlNode.text)
            solutionNode.tail = '\n'
            entryNode.append(solutionNode)
            oldShortcodesIndex += 1
            problemNumber += 1

        # Check that we covered all the shortcodes
        remainder = len(oldShortcodesNode) - problemNumber + 1
        if remainder > 0:
            one = (remainder == 1)
            message = "There %s still %i shortcode%s left after having processed %i problem%s. [Title: %s]" % \
                (['are', 'is'][one], remainder, ['s', ''][one], problemNumber-1, ['s', ''][(problemNumber-1) == 1], repr(etree.tostring(titleNode).strip()))
            raise ValueError, message

        # replace old exercise node with new exercises node
        newExercisesNode.tail = oldExerciseNode.tail
        oldExerciseNode.getparent().replace(oldExerciseNode, newExercisesNode)


def convert_to_latest(iXml):
    """
    The input argument can be either a string-like object with XML
    content or a lxml.etree Element that is the root node of the DOM.
    If the input is a string, a modified string will be returned.  If
    the input is a DOM, it will be modified *in place* and also
    returned.
    """
    if isinstance(iXml, basestring):
        # Convert to DOM
        dom = etree.fromstring(iXml)
    else:
        # Assume input is already a DOM
        dom = iXml

    # Determine XML version
    versionNodeList = dom.xpath('/document/metadata/cnxml-version')
    if len(versionNodeList) == 0:
        # Insert version number into DOM
        version = conversionChain[0]
        versionNode = etree.Element('cnxml-version')
        versionNode.text = version
        versionNode.tail = '\n    '
        metadataNode = dom.find('metadata')
        metadataNode.insert(0, versionNode)
    else:
        if len(versionNodeList) != 1:
            raise ValueError, "More than one cnxml-version node found in metadata section."
        version = versionNodeList[0].text
        if version is None:
            version = ''
        else:
            version = version.strip()

    # Find version number in conversion chain
    try:
        versionIndex = conversionChain.index(version)
    except ValueError:
        raise ValueError, "CNXML version number %s not found in conversion chain."%repr(version)

    # Apply conversion chain
    for i in range(versionIndex, len(conversionChain)-1):
        eval('v' + conversionChain[i].replace('.','_') + '_to_v' + conversionChain[i+1].replace('.','_'))(dom)

    if isinstance(iXml, basestring):
        return etree.tostring(dom, xml_declaration=True, encoding='utf-8')
    else:
        return dom


if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'rt') as fp:
        xml = fp.read()
    print convert_to_latest(xml)
