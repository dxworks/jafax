package org.vladg.jafax.repository.model

abstract class Container(
    name: String,
    modifiers: Set<Modifier>,
    container: Container?
) : ASTObject(name, modifiers, container) {

    val containedClasses: MutableSet<Class> = HashSet()

    val containedMethods: MutableSet<Method> = HashSet()

    val calledMethods: MutableSet<Method> = HashSet()

    val accessedFields: MutableSet<Attribute> = HashSet()

    fun addToContainedClasses(clazz: Class) = containedClasses.add(clazz)

    fun addToContainedMethods(method: Method) = containedMethods.add(method)

    fun addToCalledMethods(method: Method) = calledMethods.add(method)

    fun addToAccessedFields(attribute: Attribute) = accessedFields.add(attribute)

    abstract fun addToContainedAttributes(attribute: Attribute)

    abstract fun uniqueContainerIdentifier(): String

    override fun isSame(value: ASTObject) =
            value is Container &&
            super.isSame(value) &&
            containedClasses == value.containedClasses &&
            containedMethods == value.containedMethods &&
            calledMethods == value.calledMethods &&
            accessedFields == value.accessedFields

}